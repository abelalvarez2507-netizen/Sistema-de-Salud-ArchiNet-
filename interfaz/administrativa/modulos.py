
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from modelos.herencia.paciente import Paciente
from modelos.herencia.personal_salud import PersonalSalud
from modelos.herencia.personal_enfermeria import PersonalEnfermeria
from modelos.agenda.cita import Cita
from modelos.atenciones.atencion_medica import AtencionMedica
from modelos.atenciones.medicamento_recetado import MedicamentoRecetado
from servicios.validacion import (
    validar_dni as validar_dni_valor,
    validar_dni_en_edicion,
    validar_nombre_en_edicion,
)
from interfaz.campos import configurar_mascara_fecha
from interfaz.estilos import *


from interfaz.administrativa.pacientes.menus import PacientesMenusMixin
from interfaz.administrativa.pacientes.registro import PacientesRegistroMixin
from interfaz.administrativa.pacientes.consulta import PacientesConsultaMixin
from interfaz.administrativa.pacientes.historial import PacientesHistorialMixin



class AdministrativoModulosMixin:

    def _crear_modulo(self, zona, fila, columna, icono, titulo, descripcion, cantidad, detalle, texto_boton, comando):
        tarjeta = tk.Frame(
            zona,
            bg=COLOR_PANEL,
            highlightbackground=COLOR_PANEL_CLARO,
            highlightthickness=1
        )

        tarjeta.grid(
            row=fila,
            column=columna,
            sticky="nsew",
            padx=7,
            pady=7
        )

        superior = tk.Frame(
            tarjeta,
            bg=COLOR_PANEL
        )

        superior.pack(
            fill="x",
            padx=16,
            pady=(15, 5)
        )

        tk.Label(
            superior,
            text=icono,
            font=("Arial", 22, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_ROJO
        ).pack(
            side="left"
        )

        tk.Label(
            superior,
            text=titulo,
            font=FUENTE_SECCION,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            wraplength=235,
            justify="left"
        ).pack(
            side="left",
            padx=9
        )

        if descripcion:
            tk.Label(
                tarjeta,
                text=descripcion,
                font=FUENTE_PEQUENA,
                bg=COLOR_PANEL,
                fg=COLOR_GRIS,
                wraplength=290,
                justify="left"
            ).pack(
                anchor="w",
                padx=16,
                pady=(0, 10)
            )

        estadistica = tk.Frame(
            tarjeta,
            bg=COLOR_PANEL_CLARO
        )

        estadistica.pack(
            fill="x",
            padx=16,
            pady=(0, 12)
        )

        tk.Label(
            estadistica,
            text=str(cantidad),
            font=("Arial", 17, "bold"),
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO
        ).pack(
            side="left",
            padx=10,
            pady=7
        )

        tk.Label(
            estadistica,
            text=detalle,
            font=FUENTE_PEQUENA,
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_GRIS_CLARO
        ).pack(
            side="left",
            padx=(0, 8)
        )

        boton = tk.Button(
            tarjeta,
            text=texto_boton,
            command=comando,
            font=FUENTE_BOTON,
            bg=COLOR_ROJO,
            fg=COLOR_BLANCO,
            activebackground=COLOR_ROJO_CLARO,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=8,
            width=22
        )

        boton.pack(
            anchor="center",
            pady=(0, 15),
            ipadx=5
        )

        boton.bind(
            "<Enter>",
            lambda evento,
            b=boton:
            b.configure(
                bg=COLOR_ROJO_CLARO
            )
        )

        boton.bind(
            "<Leave>",
            lambda evento,
            b=boton:
            b.configure(
                bg=COLOR_ROJO
            )
        )

