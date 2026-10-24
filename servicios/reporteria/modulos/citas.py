

class ReportesCitasMixin:
    """Operaciones de citas para Reportes."""

    def reporte_citas(self):

        citas = (
            self.sistema.obtener_citas()
        )

        pendientes = list(
            filter(
                lambda cita:
                    cita.estado == "Pendiente",
                citas
            )
        )

        atendidas = list(
            filter(
                lambda cita:
                    cita.estado == "Atendida",
                citas
            )
        )

        reprogramadas = list(
            filter(
                lambda cita:
                    cita.estado == "Reprogramada",
                citas
            )
        )

        no_atendidas = list(
            filter(lambda cita: cita.estado == "No atendida", citas)
        )
        canceladas = list(
            filter(lambda cita: cita.estado == "Cancelada", citas)
        )

        return {
            "total_citas": len(citas),
            "pendientes": len(pendientes),
            "atendidas": len(atendidas),
            "reprogramadas": len(reprogramadas),
            "no_atendidas": len(no_atendidas),
            "canceladas": len(canceladas),
        }

