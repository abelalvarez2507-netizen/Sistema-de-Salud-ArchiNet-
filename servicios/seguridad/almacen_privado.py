import csv
import hashlib
import io
import json
import os
import re
import tempfile
from pathlib import Path


class DatosPrivadosUsuario:
    MAGIC = b"ARCHINET1"
    ITERACIONES = 600000
    TAMANO_SAL = 16
    TAMANO_NONCE = 12

    def __init__(self, codigo, raiz=None):
        codigo = str(codigo or "").strip().upper()
        if not codigo:
            raise ValueError("La cuenta no tiene un código de paciente válido.")
        coincidencia = re.fullmatch(r"P(\d+)", codigo)
        if coincidencia:
            identificador = str(int(coincidencia.group(1)))
        else:
            identificador = re.sub(r"[^A-Z0-9_-]", "_", codigo)
        base = Path(raiz) if raiz is not None else Path(__file__).resolve().parents[2] / "datos" / "usuarios"
        self.ruta_carpeta = base / f"usuario_{identificador}"
        self.ruta_archivo = self.ruta_carpeta / "datos.csv.enc"
        self.codigo = codigo
        self._clave = None
        self._sal = None

    @staticmethod
    def _cifrado_aes():
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        except ImportError as error:
            raise ValueError("Instala las dependencias del proyecto con: python -m pip install -r requirements.txt") from error
        return AESGCM

    @classmethod
    def _derivar_clave(cls, password, sal):
        if not isinstance(password, str) or not password:
            raise ValueError("La contraseña es obligatoria para abrir los datos privados.")
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), sal, cls.ITERACIONES, dklen=32)

    def crear(self, password, datos):
        if self.ruta_archivo.exists():
            self.abrir(password)
            return self
        self.ruta_carpeta.mkdir(parents=True, exist_ok=True)
        self._sal = os.urandom(self.TAMANO_SAL)
        self._clave = self._derivar_clave(password, self._sal)
        self.guardar(datos)
        return self

    def abrir(self, password):
        try:
            contenido = self.ruta_archivo.read_bytes()
        except FileNotFoundError:
            raise
        encabezado = len(self.MAGIC) + self.TAMANO_SAL + self.TAMANO_NONCE
        if len(contenido) <= encabezado or not contenido.startswith(self.MAGIC):
            raise ValueError("El archivo de datos privado está dañado o no es compatible.")
        inicio_sal = len(self.MAGIC)
        inicio_nonce = inicio_sal + self.TAMANO_SAL
        self._sal = contenido[inicio_sal:inicio_nonce]
        nonce = contenido[inicio_nonce:encabezado]
        self._clave = self._derivar_clave(password, self._sal)
        try:
            texto = self._cifrado_aes()(self._clave).decrypt(
                nonce,
                contenido[encabezado:],
                self._datos_asociados(),
            )
            self._leer_csv(texto.decode("utf-8"))
        except Exception as error:
            if isinstance(error, ValueError) and str(error).startswith("El archivo CSV"):
                raise
            raise ValueError("No se pudo abrir el archivo de datos privado.") from error
        return self

    def leer(self):
        if self._clave is None or self._sal is None:
            raise ValueError("Debes autenticarte para abrir los datos privados.")
        contenido = self.ruta_archivo.read_bytes()
        encabezado = len(self.MAGIC) + self.TAMANO_SAL + self.TAMANO_NONCE
        if len(contenido) <= encabezado or not contenido.startswith(self.MAGIC):
            raise ValueError("El archivo de datos privado está dañado o no es compatible.")
        nonce = contenido[len(self.MAGIC) + self.TAMANO_SAL:encabezado]
        texto = self._cifrado_aes()(self._clave).decrypt(
            nonce,
            contenido[encabezado:],
            self._datos_asociados(),
        ).decode("utf-8")
        return self._leer_csv(texto)

    def guardar(self, datos):
        if self._clave is None or self._sal is None:
            raise ValueError("Debes autenticarte para guardar los datos privados.")
        self.ruta_carpeta.mkdir(parents=True, exist_ok=True)
        salida = io.StringIO(newline="")
        escritor = csv.DictWriter(salida, fieldnames=("tipo", "datos"), delimiter=";", lineterminator="\n")
        escritor.writeheader()
        for tipo in ("perfil", "citas", "atenciones", "ventas_medicamentos"):
            valor = datos.get(tipo)
            if valor is None:
                continue
            elementos = valor if tipo != "perfil" else [valor]
            if not isinstance(elementos, list):
                elementos = [elementos]
            for elemento in elementos:
                escritor.writerow({"tipo": tipo, "datos": json.dumps(elemento, ensure_ascii=False, separators=(",", ":"))})
        escritor.writerow({"tipo": "usuario", "datos": json.dumps(datos.get("usuario", ""), ensure_ascii=False)})
        nonce = os.urandom(self.TAMANO_NONCE)
        cifrado = self._cifrado_aes()(self._clave).encrypt(
            nonce,
            salida.getvalue().encode("utf-8"),
            self._datos_asociados(),
        )
        contenido = self.MAGIC + self._sal + nonce + cifrado
        archivo_temporal = None
        try:
            with tempfile.NamedTemporaryFile(dir=self.ruta_carpeta, prefix=".datos-", suffix=".tmp", delete=False) as archivo:
                archivo_temporal = Path(archivo.name)
                archivo.write(contenido)
                archivo.flush()
                os.fsync(archivo.fileno())
            os.replace(archivo_temporal, self.ruta_archivo)
        finally:
            if archivo_temporal is not None:
                archivo_temporal.unlink(missing_ok=True)

    def _datos_asociados(self):
        return ("Archinet:" + self.codigo).encode("utf-8")

    @staticmethod
    def _leer_csv(texto):
        try:
            lector = csv.DictReader(io.StringIO(texto, newline=""), delimiter=";")
            if lector.fieldnames != ["tipo", "datos"]:
                raise ValueError
            resultado = {"perfil": {}, "citas": [], "atenciones": [], "ventas_medicamentos": [], "usuario": ""}
            for fila in lector:
                tipo = fila.get("tipo")
                dato = json.loads(fila.get("datos") or "null")
                if tipo == "perfil":
                    resultado["perfil"] = dato
                elif tipo in {"citas", "atenciones", "ventas_medicamentos"}:
                    resultado[tipo].append(dato)
                elif tipo == "usuario":
                    resultado["usuario"] = dato
                else:
                    raise ValueError
            return resultado
        except (csv.Error, json.JSONDecodeError, TypeError, ValueError) as error:
            raise ValueError("El archivo CSV privado no tiene un formato válido.") from error
