from modelos.herencia.paciente import Paciente
from modelos.herencia.personal_salud import PersonalSalud
from modelos.herencia.personal_enfermeria import PersonalEnfermeria
from modelos.agenda.cita import Cita
from modelos.atenciones.atencion_medica import AtencionMedica


from servicios.fabricacion.entidades.personas import FabricaPersonasMixin
from servicios.fabricacion.entidades.citas import FabricaCitasMixin
from servicios.fabricacion.entidades.atenciones import FabricaAtencionesMixin

class FabricaEntidades(FabricaPersonasMixin, FabricaCitasMixin, FabricaAtencionesMixin):
    """
    Factory responsable de centralizar la creación
    de objetos principales del sistema.
    """






