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




class PacienteEstructuraMixin:

    def crear_interfaz(self):

        self._limpiar_contenido()
        self._pantalla_titulo = "Inicio"
        instalar_navegacion(
            self.ventana,
            volver=self.volver_a_inicio,
            inicio=self.volver_a_inicio,
        )

        vista = VistaDesplazable(
            self.ventana,
            COLOR_FONDO,
        )
        vista.pack(fill="both", expand=True)
        contenedor = vista.contenido
        self.pantalla_actual = vista

        # =====================================================
        # BARRA SUPERIOR
        # =====================================================

        barra_superior = tk.Frame(
            contenedor,
            bg=COLOR_FONDO
        )

        barra_superior.pack(
            fill="x",
            padx=30,
            pady=(20, 10)
        )

        boton_volver = tk.Button(
            barra_superior,
            text="← Volver",
            font=FUENTE_BOTON,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            activebackground=COLOR_ROJO,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.volver_a_inicio
        )

        boton_volver.pack(
            side="left"
        )

        logo = tk.Label(
            barra_superior,
            text="ARCHINET",
            font=FUENTE_LOGO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        )

        logo.pack(
            side="right"
        )

        linea = tk.Frame(
            contenedor,
            bg=COLOR_ROJO,
            height=3
        )

        linea.pack(
            fill="x",
            padx=30,
            pady=(0, 25)
        )

        # =====================================================
        # TÍTULO
        # =====================================================

        titulo = tk.Label(
            contenedor,
            text="Portal del paciente",
            font=FUENTE_TITULO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        )

        titulo.pack(
            pady=(5, 5)
        )

        # La autenticación ocurre antes de abrir este portal; no se permite
        # cambiar a otro paciente desde una sesión ya iniciada.
        panel_identificacion = tk.Frame(contenedor, bg=COLOR_PANEL, padx=24, pady=16)
        panel_identificacion.pack(fill="x", padx=80, pady=10)
        tk.Label(
            panel_identificacion,
            text=f"{self.paciente_actual.nombre}  ·  Cuenta {self.sesion.usuario}",
            font=("Arial", 11),
            fg=COLOR_GRIS_CLARO,
            bg=COLOR_PANEL,
        ).pack()

        self.etiqueta_sesion = tk.Label(
            contenedor,
            text="",
            font=("Arial", 10, "bold"),
            fg=COLOR_GRIS_CLARO,
            bg=COLOR_FONDO,
        )
        self.etiqueta_sesion.pack(pady=(8, 15))

        # =====================================================
        # ESTADO DE SESIÓN
        # =====================================================

        # =====================================================
        # PANEL DE OPCIONES
        # =====================================================

        panel_opciones = tk.Frame(
            contenedor,
            bg=COLOR_FONDO
        )

        panel_opciones.pack(
            pady=5
        )
        panel_opciones.columnconfigure(0, weight=1, uniform="opciones_paciente")
        panel_opciones.columnconfigure(1, weight=1, uniform="opciones_paciente")

        tarjeta_citas = self.crear_tarjeta(
            panel_opciones,
            "Mis citas",
            "",
            self.mostrar_citas
        )

        tarjeta_citas.grid(
            row=0,
            column=0,
            padx=15,
            pady=10
        )

        tarjeta_historial = self.crear_tarjeta(
            panel_opciones,
            "Mi historial clínico",
            "",
            self.mostrar_historial
        )

        tarjeta_historial.grid(
            row=0,
            column=1,
            padx=15,
            pady=10
        )

        tarjeta_datos = self.crear_tarjeta(
            panel_opciones,
            "Mis datos",
            "",
            self.mostrar_datos
        )

        tarjeta_datos.grid(
            row=1,
            column=0,
            padx=15,
            pady=10
        )

        tarjeta_reservar = self.crear_tarjeta(
            panel_opciones,
            "Solicitar una cita",
            "",
            self.solicitar_cita
        )

        tarjeta_reservar.grid(
            row=1,
            column=1,
            padx=15,
            pady=10
        )
    def _limpiar_contenido(self):
        """Elimina la pantalla actual sin cerrar la ventana principal."""
        for widget in self.ventana.winfo_children():
            try:
                widget.destroy()
            except tk.TclError:
                pass

        self.pantalla_actual = None
    def _crear_pantalla_interna(self, titulo):
        """
        Crea una pantalla interna dentro del mismo Tk.
        No abre una ventana nueva.
        """
        self._limpiar_contenido()

        vista = VistaDesplazable(
            self.ventana,
            COLOR_FONDO,
        )
        vista.pack(fill="both", expand=True)
        pantalla = vista.contenido

        self.pantalla_actual = vista
        self._pantalla_titulo = titulo
        instalar_navegacion(
            self.ventana,
            volver=self.crear_interfaz,
            inicio=self.volver_a_inicio,
        )

        barra = tk.Frame(
            pantalla,
            bg=COLOR_FONDO
        )

        barra.pack(
            fill="x",
            padx=30,
            pady=(20, 10)
        )

        boton_volver = tk.Button(
            barra,
            text="← Volver",
            font=FUENTE_BOTON,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            activebackground=COLOR_ROJO,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.crear_interfaz
        )

        boton_volver.pack(
            side="left"
        )

        tk.Label(
            barra,
            text="ARCHINET",
            font=FUENTE_LOGO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(
            side="right"
        )

        tk.Frame(
            pantalla,
            bg=COLOR_ROJO,
            height=3
        ).pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        tk.Label(
            pantalla,
            text=titulo,
            font=FUENTE_TITULO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(
            pady=(5, 5)
        )

        return pantalla
    def _alternar_pantalla_completa(self, evento=None):
        try:
            actual = bool(
                self.ventana.attributes("-fullscreen")
            )

            self.ventana.attributes(
                "-fullscreen",
                not actual
            )

        except tk.TclError:

            try:
                estado = self.ventana.state()

                self.ventana.state(
                    "normal"
                    if estado == "zoomed"
                    else "zoomed"
                )

            except tk.TclError:
                pass
    def _revisar_citas_vencidas(self):
        try:
            vencidas = self.sistema.actualizar_citas_vencidas()
            if vencidas and self._pantalla_titulo == "Mis citas" and self.paciente_actual:
                self.mostrar_citas()
            self._temporizador = self.ventana.after(
                60000,
                self._revisar_citas_vencidas,
            )
        except tk.TclError:
            self._temporizador = None
    def volver_a_inicio(self):

        if self._temporizador:
            try:
                self.ventana.after_cancel(self._temporizador)
            except tk.TclError:
                pass
            self._temporizador = None

        try:
            if self.sistema is not None:
                self.sistema.cerrar()
        except Exception:
            pass

        try:
            self._limpiar_contenido()
            self.paciente_actual = None
            self.pantalla_inicio.mostrar()
        except tk.TclError:
            pass

