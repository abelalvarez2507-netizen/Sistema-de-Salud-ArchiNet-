"""Autenticación por rol para los portales de Archinet."""

from dataclasses import dataclass
import hashlib
import hmac
import os
import re
import unicodedata

from servicios.persistencia.repositorio import RepositorioSalud
from servicios.seguridad.seguridad import SeguridadDatos
from servicios.validacion import (
    validar_dni,
    validar_edad,
    validar_especialidad,
    validar_nombre,
)
from modelos.herencia.paciente import Paciente
from modelos.herencia.personal_enfermeria import PersonalEnfermeria
from modelos.herencia.personal_salud import PersonalSalud


@dataclass(frozen=True)
class SesionUsuario:
    """Identidad autenticada que se entrega al portal correspondiente."""

    rol: str
    usuario: str
    codigo_referencia: str | None = None




class AutenticacionRegistroMixin:
    """Operaciones de registro para ServicioAutenticacion."""

    def registrar(
        self,
        usuario,
        password,
        rol,
        codigo,
        dni,
        acepta_terminos=False,
        codigo_medico=None,
    ):
        """Crea una cuenta tras validar la identidad y, para personal, el código médico."""
        if not acepta_terminos:
            raise ValueError(
                "Debes aceptar los términos y condiciones para crear tu cuenta."
            )
        if rol not in {"paciente", "profesional", "enfermeria"}:
            raise ValueError("Este rol no admite el registro desde el acceso.")
        if rol in {"profesional", "enfermeria"}:
            if (
                str(codigo_medico or "").strip().casefold()
                != self.CODIGO_MEDICO_REGISTRO.casefold()
            ):
                raise ValueError("El código de autentificacion no es valida")
        usuario = self.validar_usuario(usuario)
        password = self.validar_password(password)
        codigo = str(codigo or "").strip()
        dni = validar_dni(dni)

        if rol == "paciente":
            persona = self.repositorio.obtener_datos_paciente_acceso(codigo)
            if not persona or not SeguridadDatos.verificar(
                dni, persona[2], persona[1]
            ):
                raise ValueError(
                    "No se pudo verificar el código y el DNI para este rol."
                )
            codigo_confirmado = persona[0]
        else:
            personal = self.repositorio.obtener_datos_personal_por_dni(dni)
            if not personal:
                raise ValueError(
                    "No encontramos un registro administrativo con ese DNI. "
                    "Si aún no tienes registro, usa la opción para crear uno "
                    "automáticamente."
                )
            if not self._puede_entrar(personal[3], rol):
                raise ValueError(
                    "El DNI está registrado en otra área del personal. "
                    "Selecciona el acceso que corresponde."
                )
            codigo_confirmado = personal[0]

        resumen, sal = self._proteger_password(password)
        self.repositorio.guardar_cuenta_acceso(
            usuario,
            rol,
            codigo_confirmado,
            resumen,
            sal,
        )
        try:
            return self._crear_sesion(rol, usuario, codigo_confirmado, password)
        except Exception:
            self.repositorio.eliminar_cuenta_acceso(usuario)
            raise
    def registrar_personal_nuevo(
        self,
        nombre,
        edad,
        dni,
        usuario,
        password,
        rol,
        especialidad=None,
        acepta_terminos=False,
        codigo_medico=None,
    ):
        """Registra personal nuevo sin tope y crea su cuenta de acceso."""
        if not acepta_terminos:
            raise ValueError(
                "Debes aceptar los términos y condiciones para crear tu cuenta."
            )
        if rol not in {"profesional", "enfermeria"}:
            raise ValueError("Este registro solo está disponible para personal de salud.")
        if (
            str(codigo_medico or "").strip().casefold()
            != self.CODIGO_MEDICO_REGISTRO.casefold()
        ):
            raise ValueError("El código de autentificacion no es correcta")

        nombre = validar_nombre(nombre)
        dni = validar_dni(dni)
        try:
            edad = int(str(edad).strip())
        except (TypeError, ValueError) as error:
            raise ValueError("La edad debe ser un número entero.") from error
        edad = validar_edad(edad)
        usuario = self.validar_usuario(usuario)
        password = self.validar_password(password)
        especialidad = (
            "Enfermería"
            if rol == "enfermeria"
            else validar_especialidad(especialidad)
        )

        existente = self.repositorio.obtener_datos_personal_por_dni(dni)
        if existente:
            if not self._puede_entrar(existente[3], rol):
                raise ValueError(
                    "Este DNI ya está registrado en otra área del personal."
                )
            codigo = existente[0]
            resumen, sal = self._proteger_password(password)
            self.repositorio.guardar_cuenta_acceso(
                usuario,
                rol,
                codigo,
                resumen,
                sal,
            )
            return SesionUsuario(rol, usuario, codigo)

        prefijo = "MTF" if rol == "enfermeria" else "CMP"
        ocupados = set()
        for fila in self.repositorio.obtener_personal():
            codigo_existente = str(fila[0]).upper()
            if (
                codigo_existente.startswith(prefijo)
                and codigo_existente[len(prefijo):].isdigit()
            ):
                ocupados.add(int(codigo_existente[len(prefijo):]))
        numero = 1
        while numero in ocupados:
            numero += 1
        codigo = f"{prefijo}{numero:03d}"

        personal = (
            PersonalEnfermeria(codigo, dni, nombre, edad)
            if rol == "enfermeria"
            else PersonalSalud(codigo, dni, nombre, edad, especialidad)
        )
        resumen, sal = self._proteger_password(password)
        self.repositorio.guardar_personal_con_cuenta(
            personal,
            usuario,
            rol,
            resumen,
            sal,
        )
        return SesionUsuario(rol, usuario, codigo)
    def _siguiente_codigo_paciente(self):
        """Primer código P### libre, igual que el que usa el área administrativa."""
        ocupados = set()
        for fila in self.repositorio.obtener_pacientes():
            codigo = str(fila[0]).upper()
            if codigo.startswith("P") and codigo[1:].isdigit():
                ocupados.add(int(codigo[1:]))
        numero = 1
        from servicios.seguridad.almacen_privado import DatosPrivadosUsuario

        while numero in ocupados or DatosPrivadosUsuario(f"P{numero:03d}").ruta_carpeta.exists():
            numero += 1
        return f"P{numero:03d}"
    def registrar_paciente_nuevo(
        self,
        nombre,
        edad,
        dni,
        usuario,
        password,
        acepta_terminos=False,
    ):
        """Permite que una persona se registre como paciente y cree su cuenta.

        Crea el registro del paciente (con código automático y DNI protegido)
        y su cuenta de acceso. Si algo falla, no queda nada a medias.
        """
        if not acepta_terminos:
            raise ValueError(
                "Debes aceptar los términos y condiciones para crear tu cuenta."
            )
        nombre = validar_nombre(nombre)
        try:
            edad = int(str(edad).strip())
        except ValueError:
            raise ValueError("La edad debe ser un número entero.") from None
        edad = validar_edad(edad)
        dni = validar_dni(dni)
        usuario = self.validar_usuario(usuario)
        password = self.validar_password(password)

        if self.repositorio.obtener_cuenta_acceso(usuario) is not None:
            raise ValueError("Ese usuario ya existe. Elige otro.")
        paciente_existente = next(
            (
                fila
                for fila in self.repositorio.obtener_pacientes()
                if SeguridadDatos.verificar(dni, fila[2], fila[1])
            ),
            None,
        )
        if paciente_existente:
            codigo = paciente_existente[0]
            resumen, sal = self._proteger_password(password)
            self.repositorio.guardar_cuenta_acceso(
                usuario,
                "paciente",
                codigo,
                resumen,
                sal,
            )
            try:
                return self._crear_sesion("paciente", usuario, codigo, password)
            except Exception:
                self.repositorio.eliminar_cuenta_acceso(usuario)
                raise

        codigo = self._siguiente_codigo_paciente()
        paciente = Paciente(codigo, dni, nombre, edad)
        self.repositorio.guardar_paciente(paciente)

        resumen, sal = self._proteger_password(password)
        cuenta_guardada = False
        try:
            self.repositorio.guardar_cuenta_acceso(
                usuario, "paciente", codigo, resumen, sal
            )
            cuenta_guardada = True
            return self._crear_sesion("paciente", usuario, codigo, password)
        except Exception:
            if cuenta_guardada:
                self.repositorio.eliminar_cuenta_acceso(usuario)
            self.repositorio.eliminar_paciente(codigo)
            raise
    def registrar_primer_administrador(
        self, usuario, password, acepta_terminos=False
    ):
        if not acepta_terminos:
            raise ValueError(
                "Debes aceptar los términos y condiciones para crear tu cuenta."
            )
        usuario = self.validar_usuario(usuario)
        password = self.validar_password(password)
        resumen, sal = self._proteger_password(password)
        self.repositorio.guardar_cuenta_acceso(
            usuario,
            "administrativa",
            None,
            resumen,
            sal,
            solo_primera_administrativa=True,
        )
        return SesionUsuario("administrativa", usuario)
    @staticmethod
    def _puede_entrar(especialidad, rol):
        texto = unicodedata.normalize(
            "NFKD", str(especialidad or "")
        ).encode("ascii", "ignore").decode("ascii").casefold()
        es_enfermeria = "enfermer" in texto
        if rol == "enfermeria":
            return es_enfermeria
        if rol == "profesional":
            return not es_enfermeria
        return False

