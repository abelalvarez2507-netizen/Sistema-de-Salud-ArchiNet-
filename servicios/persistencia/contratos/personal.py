from typing import Protocol

class PersonalProtocol(Protocol):
    def obtener_personal(self):
        ...

    def guardar_personal(self, profesional):
        ...

    def existe_dni_personal(self, dni):
        ...

