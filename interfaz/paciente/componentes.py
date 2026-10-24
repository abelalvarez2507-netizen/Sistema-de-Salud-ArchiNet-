import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from modelos.agenda.cita import Cita
from servicios.gestion.sistema_salud import SistemaSalud
from servicios.validacion import normalizar_fecha
from interfaz.campos import configurar_mascara_fecha
from servicios.validacion import validar_dni as validar_dni_valor

from interfaz.estilos import (
    COLOR_FONDO,
    COLOR_PANEL,
    COLOR_PANEL_CLARO,
    COLOR_ROJO,
    COLOR_ROJO_CLARO,
    COLOR_BLANCO,
    COLOR_ERROR,
    COLOR_TEXTO,
    COLOR_GRIS_CLARO,
    COLOR_GRIS,
    FUENTE_LOGO,
    FUENTE_TITULO,
    FUENTE_SUBTITULO,
    FUENTE_SECCION,
    FUENTE_BOTON
)
from interfaz.navegacion import VistaDesplazable, instalar_navegacion




class PacienteComponentesMixin:

    def _validar_busqueda_tecla(self, nuevo_valor):
        if nuevo_valor == "":
            return True
        return (
            all(
                caracter.isalnum() or caracter in "-_"
                for caracter in nuevo_valor
            )
        )
    def _validar_dni_tecla(self, nuevo_valor):
        if nuevo_valor == "":
            return True

        return (
            nuevo_valor.isdigit()
            and len(nuevo_valor) <= 8
        )
    def _cambiar_tipo_busqueda(self, valor):
        self.campo_dni.delete(
            0,
            tk.END
        )

        if valor == "DNI":
            self.etiqueta_busqueda.configure(
                text="Buscar por DNI:"
            )
        else:
            self.etiqueta_busqueda.configure(
                text="Buscar por código:"
            )

        self.campo_dni.focus_set()
    def crear_tarjeta(
        self,
        padre,
        titulo,
        descripcion,
        comando
    ):

        tarjeta = tk.Frame(
            padre,
            bg=COLOR_PANEL,
            width=280,
            height=125
        )

        tarjeta.pack_propagate(
            False
        )

        etiqueta_titulo = tk.Label(
            tarjeta,
            text=titulo,
            font=FUENTE_SECCION,
            fg=COLOR_TEXTO,
            bg=COLOR_PANEL
        )

        etiqueta_titulo.pack(
            pady=(16, 5)
        )

        if descripcion:
            etiqueta_descripcion = tk.Label(
                tarjeta,
                text=descripcion,
                font=("Arial", 10),
                fg=COLOR_GRIS_CLARO,
                bg=COLOR_PANEL,
                wraplength=230
            )
            etiqueta_descripcion.pack(pady=(0, 8))

        boton = tk.Button(
            tarjeta,
            text="Abrir",
            font=FUENTE_BOTON,
            bg=COLOR_ROJO,
            fg=COLOR_BLANCO,
            activebackground=COLOR_ROJO_CLARO,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=15,
            pady=5,
            command=comando
        )

        boton.pack(
            pady=3
        )

        boton.bind(
            "<Enter>",
            lambda evento: boton.configure(
                bg=COLOR_ROJO_CLARO
            )
        )

        boton.bind(
            "<Leave>",
            lambda evento: boton.configure(
                bg=COLOR_ROJO
            )
        )

        return tarjeta

