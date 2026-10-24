from modelos.herencia.paciente import Paciente
from modelos.herencia.personal_salud import PersonalSalud
from modelos.herencia.personal_enfermeria import PersonalEnfermeria
from modelos.agenda.cita import Cita
from modelos.atenciones.atencion_medica import AtencionMedica




class FabricaPersonasMixin:

    @staticmethod
    def crear_paciente(
        codigo,
        dni,
        nombre,
        edad
    ):
        return Paciente(
            codigo,
            dni,
            nombre,
            edad
        )
    @staticmethod
    def crear_paciente_desde_datos_protegidos(
        codigo,
        dni_hash,
        dni_salt,
        nombre,
        edad
    ):
        return Paciente.desde_datos_protegidos(
            codigo,
            dni_hash,
            dni_salt,
            nombre,
            edad
        )
    @staticmethod
    def crear_personal(
        codigo_profesional,
        dni,
        nombre,
        edad,
        especialidad
    ):
        clase = (
            PersonalEnfermeria
            if "enfermer" in str(especialidad).casefold()
            else PersonalSalud
        )
        return clase(
            codigo_profesional,
            dni,
            nombre,
            edad,
            especialidad
        )
    @staticmethod
    def crear_personal_desde_datos_protegidos(
        codigo_profesional,
        dni_hash,
        dni_salt,
        nombre,
        edad,
        especialidad
    ):
        clase = (
            PersonalEnfermeria
            if "enfermer" in str(especialidad).casefold()
            else PersonalSalud
        )
        return clase.desde_datos_protegidos(
            codigo_profesional,
            dni_hash,
            dni_salt,
            nombre,
            edad,
            especialidad
        )

