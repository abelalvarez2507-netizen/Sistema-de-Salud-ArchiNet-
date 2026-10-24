"""Pantalla de acceso y alta de cuentas dentro de la ventana principal."""
import math
import os
import tkinter as tk
from tkinter import messagebox
try:
    from PIL import Image, ImageTk
except ImportError:  # pragma: no cover
    Image = None
    ImageTk = None
from servicios.seguridad.autenticacion import ServicioAutenticacion
from servicios.validacion import (
    validar_dni_en_edicion,
    validar_nombre_en_edicion,
)
from interfaz.navegacion import VistaDesplazable
from interfaz.estilos import (
    COLOR_BLANCO,
    COLOR_FONDO,
    COLOR_GRIS,
    COLOR_GRIS_CLARO,
    COLOR_PANEL_CLARO,
    COLOR_ROJO,
    COLOR_ROJO_CLARO,
    COLOR_TEXTO,
    FUENTE_BOTON,
    FUENTE_SUBTITULO,
)

from componentes.verificacion.constantes import FUENTE_TITULO_MODAL, RUTA_FONDO, TERMINOS_CONDICIONES

class VerificadorAutenticacionMixin:

    def _iniciar_sesion(self):
        try:
            sesion = self.servicio.autenticar(
                self.campos["usuario"].get(),
                self.campos["password"].get(),
                self.rol,
            )
        except ValueError as error:
            self.error.configure(text=str(error))
            return
        if sesion is None:
            self.error.configure(text="Usuario o contraseña incorrectos para este acceso.")
            self.campos["password"].delete(0, tk.END)
            self.campos["password"].focus_set()
            return
        self._completar(sesion)
    def _completar(self, sesion):
        callback = self.al_autenticar
        self.destroy()
        callback(sesion)

