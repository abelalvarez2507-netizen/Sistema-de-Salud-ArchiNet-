

class ReportesPacientesMixin:
    """Operaciones de pacientes para Reportes."""

    def reporte_pacientes(self):

        pacientes = (
            self.sistema.obtener_pacientes()
        )

        nombres = list(
            map(
                lambda paciente:
                    paciente.nombre,
                pacientes
            )
        )

        edades = list(
            map(
                lambda paciente:
                    paciente.edad,
                pacientes
            )
        )

        return {
            "total_pacientes": len(pacientes),
            "nombres": nombres,
            "edades": edades
        }

