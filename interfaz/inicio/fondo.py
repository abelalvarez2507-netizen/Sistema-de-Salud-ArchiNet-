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




class InicioFondoMixin:

    def _cargar_imagen(self, nombre):
        """Carga una imagen de la carpeta imagenes o devuelve None."""
        if Image is None:
            return None
        try:
            imagen = Image.open(os.path.join(RUTA_IMAGENES, nombre))
            imagen.load()
            return imagen.convert("RGBA")
        except (OSError, ValueError):
            return None
    def _programar_fondo(self):
        """Redibuja el fondo poco después de dejar de cambiar el tamaño."""
        if self._fondo_original is None:
            return
        try:
            if self._after_fondo is not None:
                self._lienzo.after_cancel(self._after_fondo)
            self._after_fondo = self._lienzo.after(40, self._pintar_fondo)
        except tk.TclError:
            pass
    def _pintar_fondo(self):
        self._after_fondo = None
        if self._fondo_original is None or ImageTk is None:
            return
        try:
            ancho = self._lienzo.winfo_width()
            alto = self._lienzo.winfo_height()
        except tk.TclError:
            return
        if ancho < 50 or alto < 50 or (ancho, alto) == self._tamano_fondo:
            return

        original = self._fondo_original
        escala = max(ancho / original.width, alto / original.height)
        nuevo_ancho = math.ceil(original.width * escala)
        nuevo_alto = math.ceil(original.height * escala)
        imagen = original.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
        izquierda = (nuevo_ancho - ancho) // 2
        arriba = (nuevo_alto - alto) // 2
        imagen = imagen.crop(
            (izquierda, arriba, izquierda + ancho, arriba + alto)
        )

        try:
            self._foto_fondo = ImageTk.PhotoImage(imagen.convert("RGB"))
            self._lienzo.itemconfigure(self._id_fondo, image=self._foto_fondo)
            self._lienzo.tag_lower(self._id_fondo)
            self._tamano_fondo = (ancho, alto)
        except tk.TclError:
            pass

