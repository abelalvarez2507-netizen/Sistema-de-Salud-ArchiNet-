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

class VerificadorCuentasMixin:

    def _crear_administrador(self):
        if not self._requiere_aceptacion():
            return
        if self.campos["password"].get() != self.campos["confirmacion"].get():
            self.error.configure(text="Las contraseñas no coinciden.")
            return
        try:
            sesion = self.servicio.registrar_primer_administrador(
                self.campos["usuario"].get(),
                self.campos["password"].get(),
                acepta_terminos=True,
            )
        except ValueError as error:
            self.error.configure(text=str(error))
            return
        self._completar(sesion)
    def _crear_cuenta(self):
        if not self._requiere_aceptacion():
            return
        if self.campos["password"].get() != self.campos["confirmacion"].get():
            self.error.configure(text="Las contraseñas no coinciden.")
            return
        try:
            sesion = self.servicio.registrar(
                self.campos["usuario"].get(),
                self.campos["password"].get(),
                self.rol,
                self.campos.get("codigo").get()
                if "codigo" in self.campos
                else None,
                self.campos["dni"].get(),
                acepta_terminos=True,
                codigo_medico=(
                    self.campos["codigo_medico"].get()
                    if "codigo_medico" in self.campos
                    else None
                ),
            )
        except ValueError as error:
            self.error.configure(text=str(error))
            return
        self._completar(sesion)
    def _crear_paciente_nuevo(self):
        if not self._requiere_aceptacion():
            return
        if self.campos["password"].get() != self.campos["confirmacion"].get():
            self.error.configure(text="Las contraseñas no coinciden.")
            return
        try:
            sesion = self.servicio.registrar_paciente_nuevo(
                self.campos["nombre"].get(),
                self.campos["edad"].get(),
                self.campos["dni"].get(),
                self.campos["usuario"].get(),
                self.campos["password"].get(),
                acepta_terminos=True,
            )
        except ValueError as error:
            self.error.configure(text=str(error))
            return
        messagebox.showinfo(
            "Cuenta creada",
            f"Tu registro quedó vinculado con el código {sesion.codigo_referencia}.",
            parent=self,
        )
        self._completar(sesion)
    def _crear_personal_nuevo(self):
        if not self._requiere_aceptacion():
            return
        if self.campos["password"].get() != self.campos["confirmacion"].get():
            self.error.configure(text="Las contraseñas no coinciden.")
            return
        try:
            sesion = self.servicio.registrar_personal_nuevo(
                self.campos["nombre"].get(),
                self.campos["edad"].get(),
                self.campos["dni"].get(),
                self.campos["usuario"].get(),
                self.campos["password"].get(),
                self.rol,
                especialidad=(
                    self.especialidad_var.get()
                    if self.rol == "profesional"
                    else "Enfermería"
                ),
                acepta_terminos=True,
                codigo_medico=self.campos["codigo_medico"].get(),
            )
        except ValueError as error:
            self.error.configure(text=str(error))
            return
        messagebox.showinfo(
            "Cuenta creada",
            f"Tu registro quedó vinculado con el código {sesion.codigo_referencia}.",
            parent=self,
        )
        self._completar(sesion)
    def _mostrar_registro(self):
        self._mostrar_modo("registro")

