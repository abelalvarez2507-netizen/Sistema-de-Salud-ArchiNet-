from servicios.gestion.citas.carga import SistemaCitasCargaMixin
from servicios.gestion.citas.registro import SistemaCitasRegistroMixin
from servicios.gestion.citas.agenda import SistemaCitasAgendaMixin
from servicios.gestion.citas.seguimiento import SistemaCitasSeguimientoMixin
from servicios.gestion.citas.consultas import SistemaCitasConsultasMixin

class SistemaCitasMixin(SistemaCitasCargaMixin, SistemaCitasRegistroMixin, SistemaCitasAgendaMixin, SistemaCitasSeguimientoMixin, SistemaCitasConsultasMixin):
    """Módulo compuesto para la gestión de citas."""
