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

class VerificadorEstructuraMixin:

    def _centrar(self):
        """Reinicia el desplazamiento al cambiar el contenido del formulario."""
        self.update_idletasks()
        self._vista.canvas.yview_moveto(0)
    def _construir(self):
        nombre, descripcion = self.ROLES[self.rol]
        self._vista = VistaDesplazable(self, COLOR_FONDO)
        self._vista.pack(fill="both", expand=True)
        self._canvas = self._vista.canvas
        # El contenido desplazable original llenaba el fondo con un color
        # sólido. Ahora el Canvas sirve de escenario para la ilustración.
        self._canvas.delete(self._vista._ventana_canvas)
        self._vista.contenido.destroy()
        self._vista._ventana_canvas = None
        self._fondo_original = self._cargar_fondo()
        self._foto_fondo = None
        self._tamano_fondo = None
        self._id_fondo = self._canvas.create_image(0, 0, anchor="nw")
        self._canvas.bind("<Configure>", self._programar_ajuste, add="+")

        tarjeta = tk.Frame(
            self._canvas,
            bg=COLOR_BLANCO,
            width=540,
            padx=30,
            pady=26,
            highlightthickness=1,
            highlightbackground="#DCE8E1",
        )
        self.exterior = tarjeta
        self._panel_visible = tarjeta
        self._id_panel = self._canvas.create_window(
            0, 0, anchor="n", window=tarjeta, width=540
        )
        tarjeta.bind("<Configure>", self._programar_ajuste, add="+")

        tk.Button(
            tarjeta,
            text="←  Volver al inicio",
            command=self.destroy,
            font=("Arial", 10),
            bg=COLOR_BLANCO,
            fg=COLOR_ROJO,
            activebackground=COLOR_PANEL_CLARO,
            activeforeground=COLOR_ROJO,
            relief="flat",
            cursor="hand2",
        ).pack(anchor="w", pady=(0, 10))

        tk.Label(
            tarjeta,
            text="ARCHINET",
            font=("Arial", 17, "bold"),
            fg=COLOR_ROJO,
            bg=COLOR_BLANCO,
        ).pack(pady=(0, 14))
        tk.Frame(tarjeta, bg=COLOR_ROJO, height=3).pack(fill="x")

        self.titulo = tk.Label(
            tarjeta,
            text="",
            font=FUENTE_TITULO_MODAL,
            fg=COLOR_TEXTO,
            bg=COLOR_BLANCO,
            wraplength=390,
            justify="center",
        )
        self.titulo.pack(pady=(20, 5))
        tk.Label(
            tarjeta,
            text=f"{nombre}  ·  {descripcion}",
            font=FUENTE_SUBTITULO,
            fg=COLOR_GRIS_CLARO,
            bg=COLOR_BLANCO,
            wraplength=390,
            justify="center",
        ).pack(pady=(0, 17))

        self.formulario = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        self.formulario.pack(fill="x")
        self.error = tk.Label(
            tarjeta,
            text="",
            font=("Arial", 9),
            fg="#A33737",
            bg=COLOR_BLANCO,
            wraplength=390,
            justify="center",
        )
        self.error.pack(pady=(8, 0))
        self._mostrar_modo(self.modo)
        self._programar_ajuste()
    def _cargar_fondo(self):
        if Image is None:
            return None
        try:
            imagen = Image.open(RUTA_FONDO)
            imagen.load()
            return imagen.convert("RGB")
        except (OSError, ValueError):
            return None
    def _programar_ajuste(self, _evento=None):
        try:
            if getattr(self, "_after_ajuste", None) is not None:
                self._canvas.after_cancel(self._after_ajuste)
            self._after_ajuste = self._canvas.after_idle(self._ajustar_fondo)
        except tk.TclError:
            pass
    def _ajustar_fondo(self):
        self._after_ajuste = None
        try:
            ancho = self._canvas.winfo_width()
            alto = self._canvas.winfo_height()
            panel = self._panel_visible
            if ancho < 50 or alto < 50 or not panel.winfo_exists():
                return
            ancho_panel = max(1, min(600, ancho - 48))
            self._canvas.itemconfigure(self._id_panel, width=ancho_panel)
            panel.update_idletasks()
            alto_panel = panel.winfo_reqheight()
            alto_contenido = max(alto, alto_panel + 44)
            y = max(22, (alto - alto_panel) // 2)
            self._canvas.coords(self._id_panel, ancho // 2, y)
            self._canvas.configure(scrollregion=(0, 0, ancho, alto_contenido))
            self._pintar_fondo(ancho, alto_contenido)
        except tk.TclError:
            pass
    def _pintar_fondo(self, ancho, alto):
        if self._fondo_original is None or ImageTk is None:
            return
        if (ancho, alto) == self._tamano_fondo:
            return
        original = self._fondo_original
        escala = max(ancho / original.width, alto / original.height)
        nuevo_ancho = math.ceil(original.width * escala)
        nuevo_alto = math.ceil(original.height * escala)
        imagen = original.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
        izquierda = (nuevo_ancho - ancho) // 2
        arriba = (nuevo_alto - alto) // 2
        imagen = imagen.crop((izquierda, arriba, izquierda + ancho, arriba + alto))
        try:
            self._foto_fondo = ImageTk.PhotoImage(imagen)
            self._canvas.itemconfigure(self._id_fondo, image=self._foto_fondo)
            self._canvas.tag_lower(self._id_fondo)
            self._tamano_fondo = (ancho, alto)
        except tk.TclError:
            pass
    def _agregar_consentimiento(self):
        self.acepta_terminos = tk.BooleanVar(master=self, value=False)
        fila = tk.Frame(self.formulario, bg=COLOR_BLANCO)
        fila.pack(fill="x", pady=(8, 2))
        tk.Checkbutton(
            fila,
            text="Acepto los",
            variable=self.acepta_terminos,
            font=("Arial", 10),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            activebackground=COLOR_BLANCO,
            selectcolor=COLOR_PANEL_CLARO,
            anchor="w",
        ).pack(side="left")
        enlace = tk.Label(
            fila,
            text="términos y condiciones",
            font=("Arial", 10, "underline"),
            fg=COLOR_ROJO,
            bg=COLOR_BLANCO,
            cursor="hand2",
        )
        enlace.pack(side="left")
        enlace.bind("<Button-1>", lambda _evento: self._mostrar_terminos())
    def _mostrar_terminos(self):
        if self._pagina_terminos is not None:
            return
        self._canvas.delete(self._id_panel)
        pagina = tk.Frame(self._canvas, bg=COLOR_BLANCO, padx=22, pady=18)
        self._pagina_terminos = pagina
        self._panel_visible = pagina
        self._id_panel = self._canvas.create_window(
            0, 0, anchor="n", window=pagina, width=600
        )
        pagina.bind("<Configure>", self._programar_ajuste, add="+")
        tarjeta = tk.Frame(
            pagina,
            bg=COLOR_BLANCO,
        )
        tarjeta.pack(fill="both", expand=True)
        tk.Button(
            tarjeta,
            text="←  Volver al registro",
            command=self._cerrar_terminos,
            font=FUENTE_BOTON,
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            activebackground=COLOR_ROJO_CLARO,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            cursor="hand2",
        ).pack(anchor="w", pady=(0, 12))
        tk.Label(
            tarjeta,
            text="Términos y condiciones",
            font=("Arial", 19, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_BLANCO,
        ).pack(anchor="w", pady=(0, 10))
        texto = tk.Text(
            tarjeta,
            wrap="word",
            font=("Arial", 10),
            bg=COLOR_BLANCO,
            fg=COLOR_TEXTO,
            relief="flat",
            padx=8,
            pady=8,
            spacing1=2,
            spacing3=5,
        )
        barra = tk.Scrollbar(tarjeta, orient="vertical", command=texto.yview)
        texto.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        texto.pack(fill="both", expand=True)
        texto.insert("1.0", TERMINOS_CONDICIONES)
        texto.configure(state="disabled")
    def _cerrar_terminos(self):
        if self._pagina_terminos is not None:
            self._pagina_terminos.destroy()
            self._pagina_terminos = None
        self._panel_visible = self.exterior
        self._id_panel = self._canvas.create_window(
            0, 0, anchor="n", window=self.exterior, width=600
        )
        self._programar_ajuste()
        self._centrar()
    def _requiere_aceptacion(self):
        if self.acepta_terminos is not None and self.acepta_terminos.get():
            return True
        self.error.configure(text="Debes aceptar los términos y condiciones para crear tu cuenta.")
        return False
    def destroy(self):
        if not self._cerrado:
            self._cerrado = True
            try:
                self.servicio.cerrar()
            except Exception:
                pass
        try:
            super().destroy()
        except tk.TclError:
            pass

