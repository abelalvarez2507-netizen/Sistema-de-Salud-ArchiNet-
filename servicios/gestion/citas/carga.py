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






class SistemaCitasCargaMixin:

    def _cargar_citas(self):

        datos = (
            self._repositorio
            .obtener_citas()
        )

        for fila in datos:
            if len(fila) == 6:
                (
                    codigo,
                    paciente_codigo,
                    profesional_codigo,
                    fecha,
                    motivo,
                    estado,
                ) = fila
                hora = "09:00"
            else:
                (
                    codigo,
                    paciente_codigo,
                    profesional_codigo,
                    fecha,
                    hora,
                    motivo,
                    estado,
                ) = fila

            paciente = next(
                (
                    paciente
                    for paciente in self._pacientes
                    if paciente.codigo
                    == paciente_codigo
                ),
                None
            )

            profesional = next(
                (
                    profesional
                    for profesional in self._personal
                    if (
                        profesional.codigo_profesional
                        == profesional_codigo
                    )
                ),
                None
            )

            if paciente is None:
                raise ValueError(
                    "Se encontró una cita con "
                    "un paciente inexistente."
                )

            if profesional is None:
                raise ValueError(
                    "Se encontró una cita con "
                    "un profesional inexistente."
                )

            cita = (
                FabricaEntidades.crear_cita(
                    codigo,
                    paciente,
                    profesional,
                    fecha,
                    motivo,
                    estado,
                    hora,
                )
            )

            self._citas.append(cita)

