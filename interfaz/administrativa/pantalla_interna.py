import tkinter as tk
from interfaz.estilos import COLOR_FONDO
from interfaz.navegacion import VistaDesplazable

class PantallaInterna(tk.Frame):

    def __init__(self, master, volver_callback=None, titulo="Archinet"):
        super().__init__(
            master,
            bg=COLOR_FONDO
        )

        self._root = master
        self._volver_callback = volver_callback
        self._titulo = titulo
        self._cerrando = False
        self._vista = VistaDesplazable(self, COLOR_FONDO)
        self._vista.pack(fill="both", expand=True)

    def title(self, titulo=None):
        if titulo is not None:
            self._titulo = titulo

        return self._titulo

    def geometry(self, *_args, **_kwargs):
        return None

    def minsize(self, *_args, **_kwargs):
        return None

    def transient(self, *_args, **_kwargs):
        return None

    def register(self, *args, **kwargs):
        return self._root.register(*args, **kwargs)

    def cerrar_sin_volver(self):

        self._cerrando = True

        try:
            tk.Frame.destroy(self)
        except tk.TclError:
            pass

    def destroy(self):

        if self._cerrando:
            return

        callback = self._volver_callback

        self._cerrando = True

        try:
            tk.Frame.destroy(self)
        except tk.TclError:
            pass
        finally:
            if callback is not None:
                callback()

class ContenidoPantallaInterna(tk.Frame):

    def __init__(self, pantalla):
        self._pantalla = pantalla
        super().__init__(pantalla._vista.contenido, bg=COLOR_FONDO)
        self.pack(fill="both", expand=True, padx=24, pady=(18, 24))

    def title(self, titulo=None):
        return self._pantalla.title(titulo)

    def geometry(self, *args, **kwargs):
        return self._pantalla.geometry(*args, **kwargs)

    def minsize(self, *args, **kwargs):
        return self._pantalla.minsize(*args, **kwargs)

    def transient(self, *args, **kwargs):
        return self._pantalla.transient(*args, **kwargs)

    def register(self, *args, **kwargs):
        return self._pantalla.register(*args, **kwargs)

    def cerrar_sin_volver(self):
        self._pantalla.cerrar_sin_volver()

    def destroy(self):
        if self._pantalla._cerrando:
            tk.Frame.destroy(self)
        else:
            self._pantalla.destroy()

