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






class SistemaCitasAgendaMixin:

    def _validar_fecha_hora_futura(self, fecha_hora):
        if fecha_hora <= datetime.now():
            raise ValueError(
                "La cita debe ser posterior a la fecha y hora actuales."
            )
    def _validar_disponibilidad(
        self,
        profesional_codigo,
        fecha,
        hora,
        paciente_codigo=None,
        excluir_codigo=None,
    ):
        for cita in self._citas:
            if cita.codigo == excluir_codigo:
                continue
            if cita.estado not in {"Pendiente", "Reprogramada", "En proceso"}:
                continue
            if cita.fecha != fecha or cita.hora != hora:
                continue
            if cita.profesional.codigo_profesional == profesional_codigo:
                raise ValueError(
                    "Ese horario ya está reservado para el profesional. "
                    "Elige otro horario disponible."
                )
            if paciente_codigo and cita.paciente.codigo == paciente_codigo:
                raise ValueError(
                    "El paciente ya tiene una cita en ese horario."
                )
    def horarios_disponibles(
        self,
        profesional_codigo,
        fecha,
        excluir_codigo=None,
    ):
        from servicios.validacion import normalizar_fecha

        fecha_normalizada = normalizar_fecha(fecha)
        fecha_base = datetime.strptime(fecha_normalizada, "%d/%m/%Y").date()
        ahora = datetime.now()
        if fecha_base < ahora.date():
            return []

        ocupados = {
            cita.hora
            for cita in self._citas
            if cita.codigo != excluir_codigo
            and cita.estado in {"Pendiente", "Reprogramada", "En proceso"}
            and cita.fecha == fecha_normalizada
            and cita.profesional.codigo_profesional == profesional_codigo
        }
        disponibles = []
        for hora in self.HORARIOS_ATENCION:
            momento = datetime.strptime(
                f"{fecha_normalizada} {hora}",
                "%d/%m/%Y %H:%M",
            )
            if hora not in ocupados and momento > ahora:
                disponibles.append(hora)
        return disponibles
    def horarios_disponibles_para_cita(self, fecha, paciente_codigo=None):
        """Devuelve horas con algún médico libre; la asignación prefiere medicina general."""
        from servicios.validacion import normalizar_fecha

        fecha_normalizada = normalizar_fecha(fecha)
        medicos = [
            profesional
            for profesional in self._personal
            if "enfermer" not in profesional.especialidad.casefold()
        ]
        horarios = {
            hora
            for profesional in medicos
            for hora in self.horarios_disponibles(
                profesional.codigo_profesional,
                fecha_normalizada,
            )
        }

        if paciente_codigo:
            horarios = {
                hora
                for hora in horarios
                if not any(
                    cita.paciente.codigo == paciente_codigo
                    and cita.fecha == fecha_normalizada
                    and cita.hora == hora
                    and cita.estado in {"Pendiente", "Reprogramada", "En proceso"}
                    for cita in self._citas
                )
            }

        return sorted(horarios)
    def profesionales_disponibles_para_cita(
        self, fecha, hora, paciente_codigo=None
    ):
        """Prefiere médicos generales disponibles y usa otro médico si hace falta."""
        from servicios.validacion import normalizar_fecha, normalizar_hora

        fecha_normalizada = normalizar_fecha(fecha)
        hora_normalizada = normalizar_hora(hora)
        if hora_normalizada not in self.HORARIOS_ATENCION:
            return []

        if paciente_codigo and any(
            cita.paciente.codigo == paciente_codigo
            and cita.fecha == fecha_normalizada
            and cita.hora == hora_normalizada
            and cita.estado in {"Pendiente", "Reprogramada", "En proceso"}
            for cita in self._citas
        ):
            return []

        medicos = [
            profesional
            for profesional in self._personal
            if "enfermer" not in profesional.especialidad.casefold()
        ]
        generales = [
            profesional
            for profesional in medicos
            if profesional.especialidad.strip().casefold() == "medicina general"
        ]

        def disponibles(profesionales):
            return [
                profesional
                for profesional in profesionales
                if hora_normalizada in self.horarios_disponibles(
                    profesional.codigo_profesional,
                    fecha_normalizada,
                )
            ]

        candidatos = disponibles(generales)
        return candidatos or disponibles(medicos)
    def crear_cita_asignacion_automatica(self, paciente, fecha, motivo, hora):
        """Reserva con asignación aleatoria entre médicos que tienen ese turno libre."""
        from servicios.validacion import normalizar_fecha, normalizar_hora

        fecha_normalizada = normalizar_fecha(fecha)
        hora_normalizada = normalizar_hora(hora)
        candidatos = self.profesionales_disponibles_para_cita(
            fecha_normalizada,
            hora_normalizada,
            paciente_codigo=paciente.codigo,
        )
        if not candidatos:
            raise ValueError(
                "Ese horario ya no está disponible. Actualiza la lista y elige otro."
            )

        cita = Cita(
            self.generar_codigo_cita(),
            paciente,
            random.choice(candidatos),
            fecha_normalizada,
            motivo,
            "Pendiente",
            hora_normalizada,
        )
        self.registrar_cita(cita)
        return cita

