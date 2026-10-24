"""Herramientas comunes de desplazamiento y navegación para Archinet."""

import time
import tkinter as tk


# =========================================================
# SENSIBILIDAD DEL DESPLAZAMIENTO (ajusta aquí)
# =========================================================

# Rueda de un mouse: píxeles que baja la pantalla por cada "clic".
PIXELES_POR_CLIC = 20

# Touchpad de laptop: píxeles por cada unidad que envía el touchpad.
# Más alto = más rápido; más bajo = más lento y fino.
SENSIBILIDAD_TOUCHPAD = 0.4

# Mac: píxeles por cada unidad de desplazamiento.
PIXELES_POR_UNIDAD_MAC = 8

# Los lienzos desplazables avanzan de 1 en 1 píxel para que el touchpad se
# sienta suave. Las flechas de la barra se escalan con PIXELES_POR_CLIC.
PASO_FINO = 1

# Si llegan eventos "no múltiplos de 120", son de un touchpad: durante este
# tiempo (segundos) se sigue tratando el gesto como touchpad.
VENTANA_TOUCHPAD = 0.35


from interfaz.navegacion.desplazamiento import VistaDesplazable


def instalar_navegacion(ventana, volver=None, inicio=None):
    """Activa Alt+Izquierda para volver y Alt+Inicio para ir al inicio."""

    if not getattr(ventana, "_archinet_navegacion_instalada", False):
        ventana._archinet_navegacion_instalada = True

        def volver_teclado(_evento=None):
            secundaria = _ventana_secundaria_activa(ventana)
            if secundaria is not None:
                callback_secundario = getattr(
                    secundaria,
                    "_archinet_volver",
                    None,
                )
                if callable(callback_secundario):
                    callback_secundario()
                else:
                    secundaria.destroy()
                return "break"
            callback = getattr(ventana, "_archinet_volver", None)
            if callable(callback):
                callback()
            return "break"

        def inicio_teclado(_evento=None):
            secundaria = _ventana_secundaria_activa(ventana)
            if secundaria is not None:
                secundaria.destroy()
            callback = getattr(ventana, "_archinet_inicio", None)
            if callable(callback):
                callback()
            return "break"

        ventana.bind_all("<Alt-Left>", volver_teclado, add="+")
        ventana.bind_all("<Alt-Home>", inicio_teclado, add="+")

    if volver is not None:
        ventana._archinet_volver = volver
    if inicio is not None:
        ventana._archinet_inicio = inicio


def _ventana_secundaria_activa(ventana):
    try:
        foco = ventana.focus_get()
        if foco is None:
            return None
        secundaria = foco.winfo_toplevel()
        return secundaria if secundaria is not ventana else None
    except tk.TclError:
        return None

