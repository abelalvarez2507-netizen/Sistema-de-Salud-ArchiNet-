from typing import Protocol

class AtencionesProtocol(Protocol):
    def obtener_atenciones(self):
        ...

    def guardar_atencion(self, atencion):
        ...

    def actualizar_estado_atencion(
        self,
        codigo_atencion,
        nuevo_estado
    ):
        ...

    def actualizar_diagnostico_atencion(
        self,
        codigo_atencion,
        diagnostico,
        profesional_derivado_codigo=None,
        informe_derivacion=None,
    ):
        ...

    def guardar_recetas_atencion(self, codigo_atencion, recetas):
        ...

    def obtener_recetas_atencion(self, codigo_atencion):
        ...

