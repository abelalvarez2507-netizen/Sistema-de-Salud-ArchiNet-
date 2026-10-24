from typing import Protocol

class MedicamentosProtocol(Protocol):
    def guardar_medicamento(self, *datos):
        ...

    def obtener_medicamentos(self):
        ...

    def obtener_medicamentos_disponibles(self, fecha_actual):
        ...

    def registrar_venta_medicamento(self, *datos):
        ...

    def obtener_ventas_medicamentos(self, limite=100):
        ...

    def obtener_ventas_paciente(self, codigo_paciente):
        ...

    def obtener_estadisticas_medicamentos(self, fecha_actual):
        ...

