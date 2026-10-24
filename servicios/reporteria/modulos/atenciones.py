

class ReportesAtencionesMixin:
    """Operaciones de atenciones para Reportes."""

    def reporte_atenciones(self):

        atenciones = (
            self.sistema.obtener_atenciones()
        )

        diagnosticos = list(
            map(
                lambda atencion:
                    atencion.diagnostico,
                atenciones
            )
        )

        pendientes = list(
            filter(
                lambda atencion:
                    atencion.estado == "Pendiente",
                atenciones
            )
        )

        en_proceso = list(
            filter(
                lambda atencion:
                    atencion.estado == "En proceso",
                atenciones
            )
        )

        finalizadas = list(
            filter(
                lambda atencion:
                    atencion.estado == "Finalizada",
                atenciones
            )
        )

        return {
            "total_atenciones":
                len(atenciones),

            "diagnosticos":
                diagnosticos,

            "pendientes":
                len(pendientes),

            "en_proceso":
                len(en_proceso),

            "finalizadas":
                len(finalizadas)
        }
    def reporte_general(self):

        pacientes = (
            self.sistema.obtener_pacientes()
        )

        profesionales = (
            self.sistema.obtener_personal()
        )

        citas = (
            self.sistema.obtener_citas()
        )

        atenciones = (
            self.sistema.obtener_atenciones()
        )

        return {
            "pacientes": len(pacientes),
            "profesionales": len(profesionales),
            "citas": len(citas),
            "atenciones": len(atenciones)
        }

