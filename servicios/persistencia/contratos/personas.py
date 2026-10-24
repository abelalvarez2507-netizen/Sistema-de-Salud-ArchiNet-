from typing import Protocol

class PersonasProtocol(Protocol):
    def obtener_pacientes(self):
        ...

    def guardar_paciente(self, paciente):
        ...

    def existe_dni_paciente(self, dni):
        ...

