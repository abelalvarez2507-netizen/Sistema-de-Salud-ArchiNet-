from datetime import date
import tkinter as tk
from tkinter import messagebox

from modelos.atenciones.atencion_medica import AtencionMedica
from modelos.atenciones.medicamento_recetado import MedicamentoRecetado
from servicios.gestion.sistema_salud import SistemaSalud
from servicios.validacion import validar_diagnostico
from interfaz.campos import configurar_mascara_fecha

from interfaz.estilos import (
    COLOR_FONDO,
    COLOR_PANEL,
    COLOR_PANEL_CLARO,
    COLOR_ROJO,
    COLOR_ROJO_CLARO,
    COLOR_BLANCO,
    COLOR_TEXTO,
    COLOR_GRIS_CLARO,
    COLOR_GRIS,
    FUENTE_LOGO,
    FUENTE_TITULO,
    FUENTE_SUBTITULO,
    FUENTE_SECCION,
    FUENTE_BOTON,
)
from interfaz.navegacion import (
    PASO_FINO,
    VistaDesplazable,
    comando_barra,
    desplazar_por_evento,
    instalar_navegacion,
)




class ProfesionalEstructuraMixin:

    def _limpiar(self):
        for widget in self.ventana.winfo_children():
            try:
                widget.destroy()
            except tk.TclError:
                pass
    def _boton(self, padre, texto, comando, color=COLOR_ROJO):
        boton = tk.Button(
            padre,
            text=texto,
            command=comando,
            font=FUENTE_BOTON,
            bg=color,
            fg=(
                COLOR_BLANCO
                if color == COLOR_ROJO
                else COLOR_TEXTO
            ),
            activebackground=COLOR_ROJO_CLARO,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            cursor="hand2",
            takefocus=True,
            padx=14,
            pady=8,
        )
        boton.bind(
            "<Enter>",
            lambda evento: boton.configure(
                bg=COLOR_ROJO_CLARO,
                fg=COLOR_BLANCO,
            ),
        )
        boton.bind(
            "<Leave>",
            lambda evento: boton.configure(
                bg=color,
                fg=(
                    COLOR_BLANCO
                    if color == COLOR_ROJO
                    else COLOR_TEXTO
                ),
            ),
        )
        return boton
    def _marco_base(self, titulo, subtitulo=None, volver=None):
        self._limpiar()
        vista = VistaDesplazable(self.ventana, COLOR_FONDO)
        vista.pack(fill="both", expand=True)
        contenedor = vista.contenido
        contenedor.configure(padx=32, pady=22)
        instalar_navegacion(
            self.ventana,
            volver=volver or self.volver_a_inicio,
            inicio=self.volver_a_inicio,
        )
        barra = tk.Frame(contenedor, bg=COLOR_FONDO)
        barra.pack(fill="x", pady=(0, 18))
        self._boton(
            barra,
            "← Volver a la agenda" if volver else "← Volver al inicio",
            volver or self.volver_a_inicio,
            COLOR_PANEL,
        ).pack(side="left")
        tk.Label(
            barra,
            text="ARCHINET",
            font=FUENTE_LOGO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(side="right")
        tk.Frame(contenedor, bg=COLOR_ROJO, height=3).pack(fill="x")
        tk.Label(
            contenedor,
            text=titulo,
            font=FUENTE_TITULO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(pady=(20, 5))
        if subtitulo:
            tk.Label(
                contenedor,
                text=subtitulo,
                font=FUENTE_SUBTITULO,
                fg=COLOR_GRIS_CLARO,
                bg=COLOR_FONDO,
            ).pack(pady=(0, 15))
        return contenedor
    def _actualizar_si_activo(self):
        if self.profesional_actual is not None:
            try:
                vencidas = self.sistema.actualizar_citas_vencidas()
                if vencidas and not self._pantalla_en_edicion:
                    if self._vista_actual == "hoy":
                        self.mostrar_atenciones_hoy()
                    elif self._vista_actual == "historial":
                        self.mostrar_historial()
                    else:
                        self.mostrar_agenda()
                self._temporizador = self.ventana.after(
                    60000,
                    self._actualizar_si_activo,
                )
            except tk.TclError:
                pass
    @staticmethod
    def _enlazar_rueda(canvas, contenedor):
        def desplazar(evento):
            resultado = desplazar_por_evento(canvas, evento)
            return "break" if resultado else None

        def enlazar(widget):
            try:
                for secuencia in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
                    widget.bind(secuencia, desplazar, add="+")
                for hijo in widget.winfo_children():
                    enlazar(hijo)
            except tk.TclError:
                pass

        enlazar(canvas)
        enlazar(contenedor)
    def volver_a_inicio(self):
        if self._temporizador:
            try:
                self.ventana.after_cancel(self._temporizador)
            except tk.TclError:
                pass
        try:
            self.sistema.cerrar()
        except Exception:
            pass
        self.profesional_actual = None
        self.pantalla_inicio.mostrar()

