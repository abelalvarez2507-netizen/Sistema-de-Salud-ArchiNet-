from servicios.reporteria.modulos.pacientes import ReportesPacientesMixin
from servicios.reporteria.modulos.personal import ReportesPersonalMixin
from servicios.reporteria.modulos.citas import ReportesCitasMixin
from servicios.reporteria.modulos.atenciones import ReportesAtencionesMixin

class Reportes(ReportesPacientesMixin, ReportesPersonalMixin, ReportesCitasMixin, ReportesAtencionesMixin):

    def __init__(self, sistema):
        self.sistema = sistema

    # ==========================================
    # REPORTE DE PACIENTES
    # ==========================================


    # ==========================================
    # REPORTE DE PROFESIONALES
    # ==========================================


    # ==========================================
    # REPORTE DE CITAS
    # ==========================================


    # ==========================================
    # REPORTE DE ATENCIONES
    # ==========================================


    # ==========================================
    # REPORTE GENERAL
    # ==========================================

