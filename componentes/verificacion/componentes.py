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

class VerificadorComponentesMixin:

    def _campo(self, etiqueta, clave, secreto=False):
        fila = tk.Frame(self.formulario, bg=COLOR_BLANCO)
        compacto = self.modo.startswith("registro")
        fila.pack(fill="x", pady=3 if compacto else 6)
        tk.Label(
            fila,
            text=etiqueta,
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            bg=COLOR_BLANCO,
            anchor="w",
        ).pack(fill="x", pady=(0, 4))
        entrada = tk.Entry(
            fila,
            font=("Arial", 12),
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="flat",
            bd=0,
            show="*" if secreto else "",
        )
        entrada.pack(fill="x", ipady=6 if compacto else 8)
        if clave == "dni":
            validacion = self.register(validar_dni_en_edicion)
            entrada.configure(
                validate="key",
                validatecommand=(validacion, "%P"),
            )
        elif clave == "nombre":
            validacion = self.register(validar_nombre_en_edicion)
            entrada.configure(
                validate="key",
                validatecommand=(validacion, "%P"),
            )
        elif clave == "edad":
            validacion = self.register(
                lambda valor: valor == ""
                or (len(valor) <= 3 and valor.isascii() and valor.isdigit())
            )
            entrada.configure(
                validate="key",
                validatecommand=(validacion, "%P"),
            )
        self.campos[clave] = entrada
        return entrada
    def _boton(self, texto, comando, principal=False):
        boton = tk.Button(
            self.formulario,
            text=texto,
            command=comando,
            font=FUENTE_BOTON,
            bg=COLOR_ROJO if principal else COLOR_PANEL_CLARO,
            fg=COLOR_BLANCO if principal else COLOR_TEXTO,
            activebackground=COLOR_ROJO_CLARO,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=16,
            pady=9,
        )
        boton.pack(fill="x", pady=(10, 3))
        return boton
    def _enlace(self, texto, comando):
        enlace = tk.Label(
            self.formulario,
            text=texto,
            font=("Arial", 10, "underline"),
            fg=COLOR_ROJO,
            bg=COLOR_BLANCO,
            cursor="hand2",
        )
        enlace.pack(pady=(10, 0))
        enlace.bind("<Button-1>", lambda _evento: comando())
    def _limpiar_formulario(self):
        self.campos.clear()
        self.error.configure(text="")
        for widget in self.formulario.winfo_children():
            widget.destroy()
    def _mostrar_modo(self, modo):
        """Muestra un formulario y reajusta el tamaño de la ventana."""
        self._construir_modo(modo)
        self._centrar()
    def _construir_modo(self, modo):
        if modo == "registro" and self.rol in {"profesional", "enfermeria"}:
            modo = "registro_personal_nuevo"
        self.modo = modo
        self._limpiar_formulario()

        if modo == "login":
            self.acepta_terminos = None
            self.titulo.configure(text="INICIAR SESIÓN")
            self._campo("Usuario", "usuario")
            password = self._campo("Contraseña", "password", secreto=True)
            self._boton("Ingresar", self._iniciar_sesion, principal=True)
            if self.rol == "paciente":
                self._enlace(
                    "¿Eres nuevo?"
                    "\n Crear cuenta",
                    lambda: self._mostrar_modo("registro_nuevo"),
                )
            elif self.rol != "administrativa":
                self._enlace(
                    "¿Eres nuevo?"
                    "\n Crear cuenta",
                    lambda: self._mostrar_modo("registro_personal_nuevo"),
                )
            password.bind("<Return>", lambda _evento: self._iniciar_sesion())
            self.campos["usuario"].focus_set()
            return

        if modo == "configurar_admin":
            self.acepta_terminos = None
            self.titulo.configure(text="CONFIGURAR ACCESO ADMINISTRATIVO")
            tk.Label(
                self.formulario,
                text=(
                    "Crea la primera cuenta administrativa. Esta opción se "
                    "desactivará después de configurarla."
                ),
                font=("Arial", 10),
                fg=COLOR_GRIS,
                bg=COLOR_BLANCO,
                wraplength=390,
                justify="center",
            ).pack(pady=(0, 7))
            self._campo("Usuario", "usuario")
            self._campo("Contraseña", "password", secreto=True)
            confirmacion = self._campo(
                "Confirmar contraseña", "confirmacion", secreto=True
            )
            self._agregar_consentimiento()
            self._boton(
                "Crear cuenta administrativa",
                self._crear_administrador,
                principal=True,
            )
            confirmacion.bind(
                "<Return>", lambda _evento: self._crear_administrador()
            )
            return

        if modo == "registro_nuevo":
            self.acepta_terminos = None
            self.titulo.configure(text="CREAR MI CUENTA DE PACIENTE")
            self._campo("Nombre completo", "nombre")
            self._campo("Edad", "edad")
            self._campo("DNI", "dni")
            self._campo("Nuevo usuario", "usuario")
            self._campo("Nueva contraseña", "password", secreto=True)
            confirmacion = self._campo(
                "Confirmar contraseña", "confirmacion", secreto=True
            )
            self._agregar_consentimiento()
            tk.Label(
                self.formulario,
                text=(
                    "Si tu DNI ya está registrado, se vinculará a ese registro. "
                    "Si aún no lo está, se creará tu registro y un código "
                    "automático. El DNI lleva 8 dígitos. La contraseña debe "
                    "tener al menos 8 caracteres y un número."
                ),
                font=("Arial", 9),
                fg=COLOR_GRIS,
                bg=COLOR_BLANCO,
                wraplength=390,
                justify="center",
            ).pack(pady=(3, 0))
            self._boton(
                "Crear mi cuenta", self._crear_paciente_nuevo, principal=True
            )
            self._enlace(
                "Volver al inicio de sesión",
                lambda: self._mostrar_modo("login"),
            )
            confirmacion.bind(
                "<Return>", lambda _evento: self._crear_paciente_nuevo()
            )
            self.campos["nombre"].focus_set()
            return

        if modo == "registro_personal_nuevo":
            self.acepta_terminos = None
            self.titulo.configure(text="CREAR CUENTA DE PERSONAL")
            self._campo("Nombres y apellidos", "nombre")
            self._campo("Edad", "edad")
            self._campo("DNI", "dni")
            if self.rol == "profesional":
                tk.Label(
                    self.formulario,
                    text="Especialidad",
                    font=FUENTE_BOTON,
                    fg=COLOR_TEXTO,
                    bg=COLOR_BLANCO,
                    anchor="w",
                ).pack(fill="x", pady=(5, 2))
                especialidades = (
                    "Medicina General",
                    "Obstetricia",
                    "Odontología",
                    "Psicología",
                    "Nutrición",
                    "Medicina Familiar",
                    "Urología",
                    "Pediatría",
                    "Neurología",
                )
                self.especialidad_var = tk.StringVar(value=especialidades[0])
                tk.OptionMenu(
                    self.formulario,
                    self.especialidad_var,
                    *especialidades,
                ).pack(fill="x", pady=(0, 4))
            else:
                tk.Label(
                    self.formulario,
                    font=FUENTE_BOTON,
                    fg=COLOR_TEXTO,
                    bg=COLOR_BLANCO,
                    anchor="w",
                ).pack(fill="x", pady=(5, 2))
            self._campo("Código de autorización", "codigo_medico", secreto=True)
            self._campo("Nuevo usuario", "usuario")
            self._campo("Nueva contraseña", "password", secreto=True)
            confirmacion = self._campo(
                "Confirmar contraseña", "confirmacion", secreto=True
            )
            self._agregar_consentimiento()
            tk.Label(
                self.formulario,
                text=(
                    "Si ya tienes un registro, "
                    "se vinculará a tu cuenta; si no, se creará tu registro "
                    "con un código automático. Se requiere el código médico "
                    "autorizado."
                ),
                font=("Arial", 9),
                fg=COLOR_GRIS,
                bg=COLOR_BLANCO,
                wraplength=390,
                justify="center",
            ).pack(pady=(3, 0))
            self._boton(
                "Registrar y crear cuenta",
                self._crear_personal_nuevo,
                principal=True,
            )
            self._enlace(
                "Volver al inicio de sesión",
                lambda: self._mostrar_modo("login"),
            )
            confirmacion.bind(
                "<Return>", lambda _evento: self._crear_personal_nuevo()
            )
            self.campos["nombre"].focus_set()
            return

        self.titulo.configure(text="CREAR CUENTA DE ACCESO")
        if self.rol == "paciente":
            self._campo("Código de paciente", "codigo")
        self._campo("DNI", "dni", secreto=True)
        if self.rol in {"profesional", "enfermeria"}:
            self._campo("Código de verificacion", "codigo_medico", secreto=True)
        self._campo("Nuevo usuario", "usuario")
        self._campo("Nueva contraseña", "password", secreto=True)
        confirmacion = self._campo(
            "Confirmar contraseña", "confirmacion", secreto=True
        )
        self.acepta_terminos = None
        self._agregar_consentimiento()
        tk.Label(
            self.formulario,
            text=(
                    "El DNI debe coincidir con el registro administrativo. "
                    "Tu código de personal se asigna automáticamente; ingresa "
                    "el código médico autorizado. Usa una contraseña de 8 "
                    "caracteres como mínimo y al menos un número."
                if self.rol in {"profesional", "enfermeria"}
                else "Usa al menos 8 caracteres y un número. El DNI debe "
                "coincidir con el registro existente."
            ),
            font=("Arial", 9),
            fg=COLOR_GRIS,
            bg=COLOR_BLANCO,
            wraplength=390,
            justify="center",
        ).pack(pady=(3, 0))
        self._boton("Verificar y crear cuenta", self._crear_cuenta, principal=True)
        if self.rol == "paciente":
            self._enlace(
                "Soy paciente nuevo (crear mi registro)",
                lambda: self._mostrar_modo("registro_nuevo"),
            )
        else:
            self._enlace(
                "Soy personal nuevo (crear mi registro)",
                lambda: self._mostrar_modo("registro_personal_nuevo"),
            )
        self._enlace("Volver al inicio de sesión", lambda: self._mostrar_modo("login"))
        confirmacion.bind("<Return>", lambda _evento: self._crear_cuenta())

