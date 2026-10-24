import tkinter as tk
from interfaz.estilos.paleta import *

def crear_boton(
    parent,
    texto,
    comando,
    ancho=25,
    alto=1,
    grande=False
):
    """
    Crea un botón con el estilo visual de Archinet.

    Parámetros:
        parent   -> ventana o Frame donde aparecerá
        texto    -> texto del botón
        comando  -> función que ejecutará
        ancho    -> ancho del botón
        alto     -> alto del botón
        grande   -> utiliza un tamaño de fuente mayor
    """

    boton = tk.Button(
        parent,
        text=texto,
        command=comando,
        width=ancho,
        height=alto,

        font=(
            FUENTE_BOTON_GRANDE
            if grande
            else FUENTE_BOTON
        ),

        bg=COLOR_ROJO,
        fg=COLOR_BLANCO,

        activebackground=COLOR_ROJO_CLARO,
        activeforeground=COLOR_BLANCO,

        relief="flat",
        bd=0,

        cursor="hand2",

        padx=10,
        pady=8
    )

    return boton


def crear_boton_hover(
    parent,
    texto,
    comando,
    ancho=25,
    alto=1,
    grande=False
):
    """
    Crea un botón con efecto visual al pasar
    el mouse por encima.
    """

    boton = crear_boton(
        parent=parent,
        texto=texto,
        comando=comando,
        ancho=ancho,
        alto=alto,
        grande=grande
    )

    def entrar_mouse(evento):
        boton.configure(
            bg=COLOR_ROJO_CLARO
        )

    def salir_mouse(evento):
        boton.configure(
            bg=COLOR_ROJO
        )

    boton.bind(
        "<Enter>",
        entrar_mouse
    )

    boton.bind(
        "<Leave>",
        salir_mouse
    )

    return boton


def crear_panel(parent):
    """
    Crea un panel claro reutilizable.
    """

    panel = tk.Frame(
        parent,
        bg=COLOR_PANEL,
        bd=0,
        relief="flat"
    )

    return panel


def crear_titulo(
    parent,
    texto="ARCHINET"
):
    """
    Crea un título principal.
    """

    titulo = tk.Label(
        parent,
        text=texto,
        font=FUENTE_TITULO,
        fg=COLOR_BLANCO,
        bg=COLOR_FONDO
    )

    return titulo


def crear_subtitulo(
    parent,
    texto
):
    """
    Crea un subtítulo.
    """

    subtitulo = tk.Label(
        parent,
        text=texto,
        font=FUENTE_SUBTITULO,
        fg=COLOR_GRIS_CLARO,
        bg=COLOR_FONDO
    )

    return subtitulo


def crear_titulo_seccion(
    parent,
    texto
):
    """
    Crea un título para una sección.
    """

    titulo = tk.Label(
        parent,
        text=texto,
        font=FUENTE_SECCION,
        fg=COLOR_BLANCO,
        bg=COLOR_PANEL
    )

    return titulo


def crear_label(
    parent,
    texto,
    fondo=None,
    color=None,
    fuente=None
):
    """
    Crea un Label reutilizable.
    """

    if fondo is None:
        fondo = COLOR_FONDO

    if color is None:
        color = COLOR_TEXTO

    if fuente is None:
        fuente = FUENTE_NORMAL

    etiqueta = tk.Label(
        parent,
        text=texto,
        bg=fondo,
        fg=color,
        font=fuente
    )

    return etiqueta


def crear_entry(
    parent,
    ancho=30
):
    """
    Crea un campo de texto con el estilo de Archinet.
    """

    entrada = tk.Entry(
        parent,
        width=ancho,
        font=FUENTE_NORMAL,

        bg=COLOR_PANEL_CLARO,
        fg=COLOR_TEXTO,

        insertbackground=COLOR_TEXTO,

        relief="flat",
        bd=1,

        highlightthickness=1,
        highlightbackground=COLOR_GRIS_OSCURO,
        highlightcolor=COLOR_ROJO
    )

    return entrada


def crear_texto(
    parent,
    ancho=80,
    alto=20
):
    """
    Crea un área de texto para mostrar información.
    """

    texto = tk.Text(
        parent,
        width=ancho,
        height=alto,

        font=FUENTE_NORMAL,

        bg=COLOR_PANEL_CLARO,
        fg=COLOR_TEXTO,

        insertbackground=COLOR_TEXTO,

        relief="flat",
        bd=0,

        padx=10,
        pady=10,

        selectbackground=COLOR_ROJO,
        selectforeground=COLOR_BLANCO
    )

    return texto


def crear_barra_superior(
    parent,
    texto="ARCHINET"
):
    """
    Crea una barra superior roja/oscura.
    """

    barra = tk.Frame(
        parent,
        bg=COLOR_NEGRO,
        height=65
    )

    barra.pack_propagate(False)

    logo = tk.Label(
        barra,
        text=texto,
        font=FUENTE_LOGO,
        bg=COLOR_NEGRO,
        fg=COLOR_BLANCO
    )

    logo.pack(
        side="left",
        padx=25
    )

    return barra


def crear_linea_roja(parent):
    """
    Crea una línea decorativa roja.
    """

    linea = tk.Frame(
        parent,
        bg=COLOR_ROJO,
        height=3
    )

    return linea

