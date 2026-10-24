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






class SistemaCitasRegistroMixin:

    def generar_codigo_cita(self):

        numeros_ocupados = set()

        for cita in self._citas:

            codigo = cita.codigo.upper()

            if codigo.startswith("C"):

                try:
                    numero = int(codigo[1:])
                    numeros_ocupados.add(numero)

                except ValueError:
                    continue

        numero = 1

        while numero in numeros_ocupados:
            numero += 1

        return f"C{numero:03d}"
    def registrar_cita(self, cita):

        if not isinstance(
            cita,
            Cita
        ):
            raise TypeError(
                "El registro debe ser "
                "un objeto Cita."
            )

        paciente_existe = any(
            paciente.codigo
            == cita.paciente.codigo
            for paciente in self._pacientes
        )

        profesional_existe = any(
            profesional.codigo_profesional
            == cita.profesional.codigo_profesional
            for profesional in self._personal
        )

        if not paciente_existe:
            raise ValueError(
                "El paciente no está registrado."
            )

        if not profesional_existe:
            raise ValueError(
                "El profesional no está registrado."
            )

        codigo_existe = any(
            existente.codigo
            == cita.codigo
            for existente in self._citas
        )

        if codigo_existe:
            raise ValueError(
                "El código de cita "
                "ya está ocupado."
            )

        if cita.hora not in self.HORARIOS_ATENCION:
            raise ValueError(
                "El horario de atención es de 07:00 a 18:00, con turnos cada 30 minutos."
            )

        self._validar_fecha_hora_futura(cita.fecha_hora)
        self._validar_disponibilidad(
            cita.profesional.codigo_profesional,
            cita.fecha,
            cita.hora,
            paciente_codigo=cita.paciente.codigo,
        )

        self._repositorio.guardar_cita(
            cita
        )

        self._citas.append(
            cita
        )

