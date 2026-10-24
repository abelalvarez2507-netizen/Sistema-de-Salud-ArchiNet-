

class ReportesPersonalMixin:
    """Operaciones de personal para Reportes."""

    def reporte_profesionales(self):

        profesionales = (
            self.sistema.obtener_personal()
        )

        especialidades = list(
            map(
                lambda profesional:
                    profesional.especialidad,
                profesionales
            )
        )

        return {
            "total_profesionales":
                len(profesionales),

            "especialidades":
                especialidades
        }

