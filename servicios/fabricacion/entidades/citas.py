from modelos.herencia.paciente import Paciente
from modelos.herencia.personal_salud import PersonalSalud
from modelos.herencia.personal_enfermeria import PersonalEnfermeria
from modelos.agenda.cita import Cita
from modelos.atenciones.atencion_medica import AtencionMedica




class FabricaCitasMixin:

    @staticmethod
    def crear_cita(
        codigo,
        paciente,
        profesional,
        fecha,
        motivo,
        estado="Pendiente",
        hora="09:00",
    ):
        return Cita(
            codigo,
            paciente,
            profesional,
            fecha,
            motivo,
            estado,
            hora,
        )

