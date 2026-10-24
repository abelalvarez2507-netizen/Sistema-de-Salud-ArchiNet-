from typing import Protocol

class CitasProtocol(Protocol):
    def obtener_citas(self):
        ...

    def guardar_cita(self, cita):
        ...

    def actualizar_estado_cita(
        self,
        codigo_cita,
        nuevo_estado
    ):
        ...

    def actualizar_agenda_cita(self, codigo_cita, fecha, hora, estado):
        ...

