
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

from interfaz.administrativa.pantalla_interna import PantallaInterna, ContenidoPantallaInterna


class AdministrativoNavegacionMixin:

    def _alternar_pantalla_completa(
        self,
        evento=None
    ):

        try:

            actual = bool(
                self.ventana.attributes(
                    "-fullscreen"
                )
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

    def volver_panel_principal(self):

        actual = self._pantalla_actual

        if (
            actual is not None
            and actual is not self._pantalla_principal
        ):

            try:

                if isinstance(actual, VistaDesplazable):
                    actual.destroy()
                else:
                    if hasattr(actual, "_cerrando"):
                        actual._cerrando = True
                    tk.Frame.destroy(actual)

            except (
                tk.TclError,
                AttributeError
            ):
                pass

        if self._pantalla_principal is not None:

            try:

                self._pantalla_principal.pack(
                    fill="both",
                    expand=True
                )

                self._pantalla_principal.lift()

            except tk.TclError:
                pass

        self._pantalla_actual = (
            self._pantalla_principal
        )

        self._callback_volver_actual = (
            self.volver_panel_principal
        )
        instalar_navegacion(
            self.ventana,
            volver=self.volver_panel_principal,
            inicio=self.volver_a_inicio,
        )

    def volver_a_inicio(self):

        if self._vencimiento_after:
            try:
                self.ventana.after_cancel(self._vencimiento_after)
            except tk.TclError:
                pass
            self._vencimiento_after = None

        try:
            self.sistema.cerrar()
        except Exception:
            pass

        if self.pantalla_inicio is not None:

            actual = self._pantalla_actual
            if actual is not None and actual is not self._pantalla_principal:
                try:
                    if hasattr(actual, "cerrar_sin_volver"):
                        actual.cerrar_sin_volver()
                    else:
                        actual.destroy()
                except (tk.TclError, AttributeError):
                    pass

            self._pantalla_actual = None
            self._pantalla_principal = None
            self._callback_volver_actual = None

            self.pantalla_inicio.mostrar()

            return

        from interfaz.pantalla_inicio import PantallaInicio

        PantallaInicio(
            self.ventana
        ).mostrar()

    def _limpiar_pantalla_actual(self):

        actual = self._pantalla_actual

        if actual is None:
            return

        try:

            if actual is self._pantalla_principal:

                actual.pack_forget()

            else:

                if hasattr(
                    actual,
                    "cerrar_sin_volver"
                ):

                    actual.cerrar_sin_volver()

                else:
                    actual.destroy()

        except (
            tk.TclError,
            AttributeError
        ):
            pass

        finally:
            self._pantalla_actual = None

    def _crear_pantalla_interna(
        self,
        titulo="Archinet"
    ):

        callback = (
            self._callback_volver_actual
            or self.volver_panel_principal
        )

        self._limpiar_pantalla_actual()

        ventana = PantallaInterna(
            self.ventana,
            volver_callback=callback,
            titulo=titulo
        )

        ventana.pack(
            fill="both",
            expand=True
        )

        self._pantalla_actual = ventana
        contenido = ContenidoPantallaInterna(ventana)
        instalar_navegacion(
            self.ventana,
            volver=contenido.destroy,
            inicio=self.volver_a_inicio,
        )

        barra = tk.Frame(
            contenido,
            bg=COLOR_FONDO
        )

        barra.pack(
            fill="x",
            padx=24,
            pady=(18, 0)
        )

        boton_volver = tk.Button(
            barra,
            text="←  Volver",
            command=ventana.destroy,
            font=FUENTE_BOTON,
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            activebackground=COLOR_ROJO,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=13,
            pady=8
        )

        boton_volver.pack(
            side="left"
        )

        boton_volver.bind(
            "<Enter>",
            lambda evento:
            boton_volver.configure(
                bg=COLOR_ROJO_CLARO,
                fg=COLOR_BLANCO,
            )
        )

        boton_volver.bind(
            "<Leave>",
            lambda evento:
            boton_volver.configure(
                bg=COLOR_PANEL_CLARO,
                fg=COLOR_TEXTO,
            )
        )

        return contenido

    def _abrir_desde_menu(
        self,
        comando,
        volver_callback
    ):

        self._callback_volver_actual = (
            volver_callback
        )

        comando()

    def _crear_menu_gestion(
        self,
        titulo,
        descripcion,
        opciones,
        ancho=500,
        alto=500
    ):

        self._callback_volver_actual = (
            self.volver_panel_principal
        )
        instalar_navegacion(
            self.ventana,
            volver=self.volver_panel_principal,
            inicio=self.volver_a_inicio,
        )

        self._limpiar_pantalla_actual()

        vista = VistaDesplazable(
            self.ventana,
            COLOR_FONDO,
        )
        vista.pack(fill="both", expand=True)
        ventana = vista.contenido
        self._pantalla_actual = vista

        contenedor = tk.Frame(
            ventana,
            bg=COLOR_FONDO
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=25
        )

        barra_navegacion = tk.Frame(
            contenedor,
            bg=COLOR_FONDO
        )

        barra_navegacion.pack(
            fill="x",
            pady=(0, 8)
        )

        boton_panel = tk.Button(
            barra_navegacion,
            text="←  Volver",
            command=self.volver_panel_principal,
            font=FUENTE_BOTON,
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            activebackground=COLOR_ROJO,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=7
        )

        boton_panel.pack(
            side="left"
        )

        boton_panel.bind(
            "<Enter>",
            lambda evento:
            boton_panel.configure(
                bg=COLOR_ROJO_CLARO,
                fg=COLOR_BLANCO,
            )
        )

        boton_panel.bind(
            "<Leave>",
            lambda evento:
            boton_panel.configure(
                bg=COLOR_PANEL_CLARO,
                fg=COLOR_TEXTO,
            )
        )

        tk.Label(
            contenedor,
            text=titulo.upper(),
            font=FUENTE_TITULO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(
            pady=(5, 6)
        )

        if descripcion:
            tk.Label(
                contenedor,
                text=descripcion,
                font=FUENTE_SUBTITULO,
                bg=COLOR_FONDO,
                fg=COLOR_GRIS,
                wraplength=650,
                justify="center"
            ).pack(
                pady=(0, 20)
            )

        tk.Frame(
            contenedor,
            bg=COLOR_ROJO,
            height=2
        ).pack(
            fill="x",
            pady=(0, 18)
        )

        def ejecutar_opcion(
            comando
        ):

            # Al entrar a un submódulo,
            # Volver reconstruye exactamente este menú.
            callback_menu = (
                lambda:
                self._crear_menu_gestion(
                    titulo,
                    descripcion,
                    opciones,
                    ancho,
                    alto
                )
            )

            self._abrir_desde_menu(
                comando,
                callback_menu
            )

        for texto_boton, comando in opciones:

            boton = tk.Button(
                contenedor,
                text=texto_boton,
                command=lambda c=comando:
                ejecutar_opcion(c),
                font=FUENTE_BOTON_GRANDE,
                bg=COLOR_ROJO,
                fg=COLOR_BLANCO,
                activebackground=COLOR_ROJO_CLARO,
                activeforeground=COLOR_BLANCO,
                relief="flat",
                bd=0,
                cursor="hand2",
                width=30,
                pady=10
            )

            boton.pack(
                pady=6
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

        return ventana

