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






class SistemaCitasConsultasMixin:
    """Funciones de consultas de la agenda."""

    def obtener_citas(self):
        return list(self._citas)
    def obtener_citas_pendientes(self):

        return list(
            filter(
                lambda cita:
                    cita.estado == "Pendiente",
                self._citas
            )
        )
    def obtener_citas_atendidas(self):

        return list(
            filter(
                lambda cita:
                    cita.estado == "Atendida",
                self._citas
            )
        )
    def obtener_citas_reprogramadas(self):

        return list(
            filter(
                lambda cita:
                    cita.estado == "Reprogramada",
                self._citas
            )
        )
    def total_citas(self):
        return len(self._citas)
    def total_citas_pendientes(self):
        return len(
            self.obtener_citas_pendientes()
        )
    def total_citas_atendidas(self):
        return len(
            self.obtener_citas_atendidas()
        )
    def total_citas_reprogramadas(self):
        return len(
            self.obtener_citas_reprogramadas()
        )

