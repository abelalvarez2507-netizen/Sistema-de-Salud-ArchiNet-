"""Pantalla vacía de inicio para el área de triaje."""

import tkinter as tk

from interfaz.estilos import (
    COLOR_BLANCO,
    COLOR_FONDO,
    COLOR_GRIS,
    COLOR_PANEL_CLARO,
    COLOR_ROJO,
    COLOR_TEXTO,
    FUENTE_BOTON,
    FUENTE_LOGO,
    FUENTE_SUBTITULO,
    FUENTE_TITULO,
)
from interfaz.navegacion import VistaDesplazable, instalar_navegacion


class PantallaTriaje:
    """Confirma el acceso y deja el espacio de trabajo sin módulos."""

    def __init__(self, ventana, pantalla_inicio, sesion):
        if sesion is None or sesion.rol != "triaje":
            raise ValueError("Se requiere una sesión de triaje autenticada.")

        self.ventana = ventana
        self.pantalla_inicio = pantalla_inicio
        self.sesion = sesion
        self.ventana.title("Archinet - Área de Triaje")
        self.ventana.configure(bg=COLOR_FONDO)
        self.mostrar_inicio()

    def cerrar_sesion(self):
        self.pantalla_inicio.mostrar()

    def cambiar_area(self):
        """Regresa al selector de ventas y triaje."""
        self.pantalla_inicio.mostrar_selector_enfermeria()

    def mostrar_inicio(self):
        for widget in self.ventana.winfo_children():
            try:
                widget.destroy()
            except tk.TclError:
                pass

        instalar_navegacion(
            self.ventana,
            volver=self.cambiar_area,
            inicio=self.cerrar_sesion,
        )
        vista = VistaDesplazable(self.ventana, COLOR_FONDO)
        vista.pack(fill="both", expand=True)
        contenido = vista.contenido
        contenido.configure(padx=24, pady=18)

        barra = tk.Frame(contenido, bg=COLOR_FONDO)
        barra.pack(fill="x", pady=(0, 12))
        tk.Button(
            barra,
            text="↔  Cambiar de área",
            command=self.cambiar_area,
            font=FUENTE_BOTON,
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=8,
        ).pack(side="left")
        tk.Button(
            barra,
            text="Cerrar sesión",
            command=self.cerrar_sesion,
            font=FUENTE_BOTON,
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=8,
        ).pack(side="right")
        tk.Label(
            barra,
            text="ARCHINET",
            font=FUENTE_LOGO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(side="right", padx=(0, 18))
        tk.Frame(contenido, bg=COLOR_ROJO, height=3).pack(fill="x", pady=(0, 24))

        tk.Label(
            contenido,
            text="Área de triaje",
            font=FUENTE_TITULO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(anchor="w", pady=(0, 6))
        tk.Label(
            contenido,
            text=f"Sesión iniciada · {self.sesion.usuario}",
            font=FUENTE_SUBTITULO,
            fg=COLOR_GRIS,
            bg=COLOR_FONDO,
        ).pack(anchor="w")
