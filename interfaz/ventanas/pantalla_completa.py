"""Window keyboard actions shared by Archinet screens."""
import tkinter as tk

def alternar_pantalla_completa(ventana, evento=None):
    try:
        actual = bool(ventana.attributes("-fullscreen"))
        ventana.attributes("-fullscreen", not actual)
    except tk.TclError:
        try:
            estado = ventana.state()
            ventana.state("normal" if estado == "zoomed" else "zoomed")
        except tk.TclError:
            pass
