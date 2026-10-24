import tkinter as tk
from tkinter import ttk
from interfaz.estilos.paleta import *

def configurar_ventana(ventana):
    """
    Configura los aspectos visuales generales de una ventana.
    """

    ventana.configure(
        bg=COLOR_FONDO
    )


def configurar_estilos():
    """
    Configura los estilos generales utilizados por Archinet.
    """

    estilo = ttk.Style()

    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass

    # -----------------------------------------------------
    # BOTÓN PRINCIPAL
    # -----------------------------------------------------

    estilo.configure(
        "Archinet.TButton",
        font=FUENTE_BOTON,
        foreground=COLOR_BLANCO,
        background=COLOR_ROJO,
        padding=(18, 10),
        borderwidth=0,
        relief="flat"
    )

    estilo.map(
        "Archinet.TButton",
        background=[
            ("active", COLOR_ROJO_CLARO),
            ("pressed", COLOR_ROJO_OSCURO)
        ],
        foreground=[
            ("disabled", COLOR_GRIS_OSCURO),
            ("!disabled", COLOR_BLANCO)
        ]
    )

    # -----------------------------------------------------
    # BOTÓN GRANDE
    # -----------------------------------------------------

    estilo.configure(
        "Archinet.Grande.TButton",
        font=FUENTE_BOTON_GRANDE,
        foreground=COLOR_BLANCO,
        background=COLOR_ROJO,
        padding=(25, 15),
        borderwidth=0,
        relief="flat"
    )

    estilo.map(
        "Archinet.Grande.TButton",
        background=[
            ("active", COLOR_ROJO_CLARO),
            ("pressed", COLOR_ROJO_OSCURO)
        ]
    )

    # -----------------------------------------------------
    # LABEL NORMAL
    # -----------------------------------------------------

    estilo.configure(
        "Archinet.TLabel",
        background=COLOR_FONDO,
        foreground=COLOR_TEXTO,
        font=FUENTE_NORMAL
    )

    # -----------------------------------------------------
    # LABEL DE TÍTULO
    # -----------------------------------------------------

    estilo.configure(
        "Archinet.Titulo.TLabel",
        background=COLOR_FONDO,
        foreground=COLOR_TEXTO,
        font=FUENTE_TITULO
    )

    # -----------------------------------------------------
    # LABEL DE SUBTÍTULO
    # -----------------------------------------------------

    estilo.configure(
        "Archinet.Subtitulo.TLabel",
        background=COLOR_FONDO,
        foreground=COLOR_GRIS_CLARO,
        font=FUENTE_SUBTITULO
    )

    # -----------------------------------------------------
    # LABEL DE SECCIÓN
    # -----------------------------------------------------

    estilo.configure(
        "Archinet.Seccion.TLabel",
        background=COLOR_PANEL,
        foreground=COLOR_TEXTO,
        font=FUENTE_SECCION
    )

    # -----------------------------------------------------
    # ENTRY
    # -----------------------------------------------------

    estilo.configure(
        "Archinet.TEntry",
        font=FUENTE_NORMAL,
        fieldbackground=COLOR_PANEL_CLARO,
        foreground=COLOR_TEXTO,
        insertcolor=COLOR_TEXTO,
        borderwidth=1,
        padding=8
    )

    # -----------------------------------------------------
    # COMBOBOX
    # -----------------------------------------------------

    estilo.configure(
        "Archinet.TCombobox",
        font=FUENTE_NORMAL,
        fieldbackground=COLOR_PANEL_CLARO,
        background=COLOR_PANEL_CLARO,
        foreground=COLOR_TEXTO,
        borderwidth=1,
        padding=7
    )

    # -----------------------------------------------------
    # NOTEBOOK
    # -----------------------------------------------------

    estilo.configure(
        "Archinet.TNotebook",
        background=COLOR_FONDO,
        borderwidth=0
    )

    estilo.configure(
        "Archinet.TNotebook.Tab",
        font=FUENTE_NORMAL_BOLD,
        background=COLOR_PANEL,
        foreground=COLOR_GRIS_CLARO,
        padding=(15, 8)
    )

    estilo.map(
        "Archinet.TNotebook.Tab",
        background=[
            ("selected", COLOR_ROJO)
        ],
        foreground=[
            ("selected", COLOR_BLANCO)
        ]
    )


def inicializar_estilos(ventana):
    """
    Función general para iniciar los estilos de Archinet.
    """

    configurar_ventana(
        ventana
    )

    configurar_estilos()

