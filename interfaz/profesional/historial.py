from datetime import date
import tkinter as tk
from tkinter import messagebox

from modelos.atenciones.atencion_medica import AtencionMedica
from modelos.atenciones.medicamento_recetado import MedicamentoRecetado
from servicios.gestion.sistema_salud import SistemaSalud
from servicios.validacion import validar_diagnostico
from interfaz.campos import configurar_mascara_fecha

from interfaz.estilos import (
    COLOR_FONDO,
    COLOR_PANEL,
    COLOR_PANEL_CLARO,
    COLOR_ROJO,
    COLOR_ROJO_CLARO,
    COLOR_BLANCO,
    COLOR_TEXTO,
    COLOR_GRIS_CLARO,
    COLOR_GRIS,
    FUENTE_LOGO,
    FUENTE_TITULO,
    FUENTE_SUBTITULO,
    FUENTE_SECCION,
    FUENTE_BOTON,
)
from interfaz.navegacion import (
    PASO_FINO,
    VistaDesplazable,
    comando_barra,
    desplazar_por_evento,
    instalar_navegacion,
)




class ProfesionalHistorialMixin:

    def mostrar_historial(self):
        self._pantalla_en_edicion = False
        self._vista_actual = "historial"
        self.sistema.actualizar_citas_vencidas()
        contenido = self._marco_base(
            "Historial y derivaciones",
            "",
            volver=self.mostrar_agenda,
        )
        citas = []
        for cita in self._citas_para_profesional():
            atencion = self._atencion_de(cita)
            if (
                self._derivada_a_otro(cita)
                or (atencion and atencion.estado == "Finalizada")
                or cita.estado in {"Atendida", "No atendida", "Cancelada"}
            ):
                citas.append(cita)
        citas.sort(key=lambda cita: cita.fecha_hora, reverse=True)
        if not citas:
            tk.Label(
                contenido,
                text="Todavía no hay atenciones en el historial.",
                font=FUENTE_SUBTITULO,
                fg=COLOR_GRIS,
                bg=COLOR_FONDO,
            ).pack(anchor="w", pady=20)
        for cita in citas:
            self._tarjeta_cita_profesional(contenido, cita)

