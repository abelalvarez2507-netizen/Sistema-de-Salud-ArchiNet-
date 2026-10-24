from modelos.herencia.paciente import Paciente
from modelos.herencia.personal_salud import PersonalSalud
from modelos.herencia.personal_enfermeria import PersonalEnfermeria
from modelos.agenda.cita import Cita
from modelos.atenciones.atencion_medica import AtencionMedica




class FabricaAtencionesMixin:

    @staticmethod
    def crear_atencion(
        codigo,
        cita,
        diagnostico,
        estado="Pendiente",
        recetas=None,
        profesional_derivado=None,
        informe_derivacion="",
    ):
        return AtencionMedica(
            codigo,
            cita,
            diagnostico,
            estado,
            recetas,
            profesional_derivado,
            informe_derivacion,
        )

