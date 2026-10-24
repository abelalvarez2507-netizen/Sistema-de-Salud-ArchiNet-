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




class PacientePerfilMixin:

    def mostrar_datos(self):

        if not self.paciente_autenticado():
            return

        paciente = self.paciente_actual

        ventana = self._crear_pantalla_interna(
            "Mis datos"
        )

        panel = tk.Frame(
            ventana,
            bg=COLOR_PANEL
        )

        panel.pack(
            padx=40,
            pady=15,
            fill="both",
            expand=True
        )

        datos = [
            (
                "Código",
                paciente.codigo
            ),
            (
                "Nombre",
                paciente.nombre
            ),
            (
                "Edad",
                str(paciente.edad)
            ),
            (
                "DNI",
                "********"
            )
        ]

        for etiqueta, valor in datos:

            fila = tk.Frame(
                panel,
                bg=COLOR_PANEL
            )

            fila.pack(
                fill="x",
                padx=30,
                pady=9
            )

            tk.Label(
                fila,
                text=f"{etiqueta}:",
                font=FUENTE_BOTON,
                fg=COLOR_GRIS_CLARO,
                bg=COLOR_PANEL,
                width=12,
                anchor="w"
            ).pack(
                side="left"
            )

            tk.Label(
                fila,
                text=valor,
                font=FUENTE_BOTON,
                fg=COLOR_TEXTO,
                bg=COLOR_PANEL,
                anchor="w"
            ).pack(
                side="left"
            )

