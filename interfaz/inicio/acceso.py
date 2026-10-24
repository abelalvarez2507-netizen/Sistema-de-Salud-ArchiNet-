import math
import os
import tkinter as tk
import tkinter.font as tkfont

try:  # Pillow solo se usa para el fondo decorativo; si falta, se usa color liso.
    from PIL import Image, ImageTk
except ImportError:  # pragma: no cover
    Image = None
    ImageTk = None

from interfaz.estilos import (
    COLOR_FONDO,
    COLOR_PANEL,
    COLOR_PANEL_CLARO,
    COLOR_ROJO,
    COLOR_ROJO_CLARO,
    COLOR_ROJO_OSCURO,
    COLOR_BLANCO,
    COLOR_TEXTO,
    COLOR_GRIS_CLARO,
    COLOR_GRIS,
    FUENTE_TITULO,
    FUENTE_SUBTITULO,
    FUENTE_BOTON_GRANDE
)
from interfaz.navegacion import VistaDesplazable, instalar_navegacion

RUTA_IMAGENES = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "imagenes",
)

# Color de la imagen de fondo (se usa mientras carga o si no hay Pillow).
COLOR_LIENZO_IMAGEN = "#F9FAFC"

# Colores del logo Archinet (azul y verde de la imagen de referencia).
COLOR_LOGO_AZUL = "#1B7FC4"
COLOR_LOGO_VERDE = "#1E9F5F"
COLOR_LINEA_LOGO = "#4CAF73"
FUENTE_LOGO_INICIO = ("Arial", 38, "bold")
ALTO_ICONO = 120




class InicioAccesoMixin:

    def abrir_paciente(self):
        self._solicitar_acceso("paciente")
    def abrir_administrativa(self):
        self._solicitar_acceso("administrativa")
    def abrir_profesional(self):
        """Abre el portal privado del profesional de salud."""
        self._solicitar_acceso("profesional")
    def abrir_enfermeria(self):
        """Abre el portal de acceso restringido para enfermería."""
        self._solicitar_acceso("enfermeria")
    def _solicitar_acceso(self, rol):
        from componentes.modal_verificador import ModalVerificador

        ModalVerificador(self.ventana, rol, self._acceso_concedido)
    def _acceso_concedido(self, sesion):
        for widget in self.ventana.winfo_children():
            try:
                widget.destroy()
            except tk.TclError:
                pass

        if sesion.rol == "paciente":
            from interfaz.pantalla_paciente import PantallaPaciente

            PantallaPaciente(self.ventana, self, sesion)
        elif sesion.rol == "administrativa":
            from interfaz.pantalla_administrativa import VentanaPrincipal

            VentanaPrincipal(
                self.ventana,
                pantalla_inicio=self,
                sesion=sesion,
            )
        elif sesion.rol == "profesional":
            from interfaz.pantalla_profesional import PantallaProfesional

            PantallaProfesional(self.ventana, self, sesion)
        elif sesion.rol == "enfermeria":
            from interfaz.pantalla_enfermeria import PantallaEnfermeria

            PantallaEnfermeria(self.ventana, self, sesion)
    def salir(self):
        """Cierra completamente Archinet y todas sus ventanas."""
        try:
            self.ventana.quit()
        except tk.TclError:
            pass

        try:
            self.ventana.destroy()
        except tk.TclError:
            pass

