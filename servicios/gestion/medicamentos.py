from modelos.herencia.paciente import Paciente
from modelos.agenda.cita import Cita
from modelos.herencia.personal_salud import PersonalSalud
from modelos.atenciones.atencion_medica import AtencionMedica
from modelos.atenciones.medicamento_recetado import MedicamentoRecetado
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import random

from servicios.persistencia.repositorio import RepositorioSalud
from servicios.fabricacion.fabrica import FabricaEntidades
from servicios.persistencia.contratos import RepositorioSaludProtocol




class SistemaMedicamentosMixin:

    @staticmethod
    def _validar_recetas(recetas):
        resultado = []
        for receta in recetas or []:
            if isinstance(receta, MedicamentoRecetado):
                resultado.append(receta)
            else:
                resultado.append(MedicamentoRecetado(*receta))
        return resultado
    @staticmethod
    def _entero_no_negativo(valor, etiqueta):
        try:
            numero = int(str(valor).strip())
        except (TypeError, ValueError):
            raise ValueError(f"{etiqueta} debe ser un número entero.") from None
        if numero < 0:
            raise ValueError(f"{etiqueta} no puede ser negativo.")
        return numero
    @staticmethod
    def _precio_medicamento(valor):
        try:
            texto = str(valor).strip()
            if "," in texto and "." not in texto:
                texto = texto.replace(",", ".")
            precio = Decimal(texto).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("El precio debe ser un importe válido.") from None
        if not precio.is_finite() or precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        return float(precio)
    def registrar_medicamento(
        self,
        nombre,
        principio_activo,
        presentacion,
        lote,
        vencimiento,
        stock,
        stock_minimo,
        precio_venta,
        registrado_por,
        fecha_fabricacion=None,
    ):
        nombre = str(nombre or "").strip()
        principio_activo = str(principio_activo or "").strip()
        presentacion = str(presentacion or "").strip()
        lote = str(lote or "").strip()
        registrado_por = str(registrado_por or "").strip()
        if not nombre:
            raise ValueError("Ingresa el nombre del medicamento.")
        if not lote:
            raise ValueError("Ingresa el número de lote.")
        if not registrado_por:
            raise ValueError("No se pudo identificar a quien registra el medicamento.")
        def normalizar_fecha(valor, etiqueta):
            texto = str(valor or "").strip()
            for formato in ("%d/%m/%Y", "%Y-%m-%d"):
                try:
                    return datetime.strptime(texto, formato).date()
                except (TypeError, ValueError):
                    continue
            raise ValueError(f"Usa la fecha de {etiqueta} DD/MM/AAAA.")

        fecha_vencimiento = normalizar_fecha(vencimiento, "vencimiento")
        vencimiento = fecha_vencimiento.isoformat()
        stock = self._entero_no_negativo(stock, "El stock")
        if stock == 0:
            raise ValueError("El stock inicial debe ser mayor que cero.")
        stock_minimo = self._entero_no_negativo(
            stock_minimo, "El stock mínimo"
        )
        if fecha_vencimiento < date.today():
            raise ValueError("La fecha de vencimiento no puede estar en el pasado.")
        precio_venta = self._precio_medicamento(precio_venta)
        return self._repositorio.guardar_medicamento(
            nombre,
            principio_activo,
            presentacion,
            lote,
            vencimiento,
            stock,
            stock_minimo,
            precio_venta,
            registrado_por,
        )
    def obtener_medicamentos(self):
        return self._repositorio.obtener_medicamentos()
    def obtener_medicamentos_disponibles(self):
        return self._repositorio.obtener_medicamentos_disponibles(
            date.today().isoformat()
        )
    def vender_medicamento(self, medicamento_id, cantidad, paciente_codigo, vendido_por):
        try:
            medicamento_id = int(medicamento_id)
        except (TypeError, ValueError):
            raise ValueError("Selecciona un medicamento registrado.") from None
        if medicamento_id <= 0:
            raise ValueError("Selecciona un medicamento registrado.")
        cantidad = self._entero_no_negativo(cantidad, "La cantidad")
        if cantidad == 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        paciente_codigo = str(paciente_codigo or "").strip()
        paciente = next(
            (p for p in self._pacientes if p.codigo.casefold() == paciente_codigo.casefold()),
            None,
        )
        if paciente is None:
            raise ValueError("Ingresa el código de un paciente registrado.")
        vendido_por = str(vendido_por or "").strip()
        if not vendido_por:
            raise ValueError("No se pudo identificar a quien registra la venta.")
        return self._repositorio.registrar_venta_medicamento(
            medicamento_id,
            cantidad,
            paciente.codigo,
            vendido_por,
            datetime.now().isoformat(timespec="seconds"),
        )
    def obtener_ventas_medicamentos(self, limite=100):
        return self._repositorio.obtener_ventas_medicamentos(limite)
    def obtener_estadisticas_medicamentos(self):
        return self._repositorio.obtener_estadisticas_medicamentos(
            date.today().isoformat()
        )

