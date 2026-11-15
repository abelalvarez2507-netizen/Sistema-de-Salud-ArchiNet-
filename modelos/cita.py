from datetime import datetime

from modelos.paciente import Paciente
from modelos.personal_salud import PersonalSalud
from servicios.validaciones import (
    normalizar_fecha,
    normalizar_hora,
    validar_codigo,
    validar_motivo,
)

_FECHA_GENERACION_AHORA = object()


class Cita:
    """Representa una cita entre un paciente y un profesional."""

    TIPOS_VALIDOS = {
        "Directa",
        "Regular",
        "Consulta general",
        "Derivación urgente",
    }

    ESTADOS_VALIDOS = {
        "Pendiente",
        "En proceso",
        "Atendida",
        "Reprogramada",
        "No atendida",
        "Cancelada",
    }

    def __init__(
        self,
        codigo,
        paciente,
        profesional,
        fecha,
        motivo,
        estado="Pendiente",
        hora="09:00",
        fecha_generacion=_FECHA_GENERACION_AHORA,
        tipo_cita="Directa",
        cita_origen_codigo=None,
    ):
        if paciente is None or not isinstance(paciente, Paciente):
            raise ValueError("La cita debe tener un paciente válido.")
        if profesional is None or not isinstance(profesional, PersonalSalud):
            raise ValueError("La cita debe tener un profesional válido.")

        self._codigo = validar_codigo(codigo, "El código de la cita")
        self._paciente = paciente
        self._profesional = profesional
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo
        self.estado = estado
        self.tipo_cita = tipo_cita
        self.cita_origen_codigo = cita_origen_codigo
        if fecha_generacion is _FECHA_GENERACION_AHORA:
            self._fecha_generacion = datetime.now()
        else:
            self.fecha_generacion = fecha_generacion

    @property
    def codigo(self):
        return self._codigo

    @property
    def paciente(self):
        return self._paciente

    @property
    def profesional(self):
        return self._profesional

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = normalizar_fecha(valor)

    @property
    def hora(self):
        return self._hora

    @hora.setter
    def hora(self, valor):
        self._hora = normalizar_hora(valor)

    @property
    def fecha_hora(self):
        return datetime.strptime(
            f"{self.fecha} {self.hora}",
            "%d/%m/%Y %H:%M",
        )

    @property
    def fecha_generacion(self):
        return self._fecha_generacion

    @fecha_generacion.setter
    def fecha_generacion(self, valor):
        if valor is None or isinstance(valor, datetime):
            self._fecha_generacion = valor
            return

        texto = str(valor).strip()
        try:
            self._fecha_generacion = datetime.fromisoformat(texto)
        except ValueError:
            try:
                self._fecha_generacion = datetime.strptime(
                    texto,
                    "%d/%m/%Y %H:%M:%S",
                )
            except ValueError as error:
                raise ValueError(
                    "La fecha de generación de la cita no es válida."
                ) from error

    @property
    def motivo(self):
        return self._motivo

    @motivo.setter
    def motivo(self, valor):
        self._motivo = validar_motivo(valor)

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        if valor == "Reprogramar":
            valor = "Reprogramada"
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(
                "Estado inválido. Use: Pendiente, En proceso, Atendida, Reprogramada, "
                "No atendida o Cancelada."
            )
        self._estado = valor

    @property
    def tipo_cita(self):
        return self._tipo_cita

    @tipo_cita.setter
    def tipo_cita(self, valor):
        if valor not in self.TIPOS_VALIDOS:
            raise ValueError("El tipo de cita no es válido.")
        self._tipo_cita = valor

    @property
    def cita_origen_codigo(self):
        return self._cita_origen_codigo

    @cita_origen_codigo.setter
    def cita_origen_codigo(self, valor):
        self._cita_origen_codigo = (
            validar_codigo(valor, "El código de la cita relacionada")
            if valor
            else None
        )

    def mostrar_informacion(self):
        return (
            f"Cita: {self.codigo} | "
            f"Paciente: {self.paciente.nombre} | "
            f"Profesional: {self.profesional.nombre} | "
            f"Fecha: {self.fecha} | "
            f"Hora: {self.hora} | "
            f"Tipo: {self.tipo_cita} | "
            f"Motivo: {self.motivo} | "
            f"Estado: {self.estado}"
        )
