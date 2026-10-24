
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



class AdministrativoDashboardMixin:

    def crear_interfaz(self):

        self.sistema.actualizar_citas_vencidas()
        instalar_navegacion(
            self.ventana,
            volver=self.volver_a_inicio,
            inicio=self.volver_a_inicio,
        )

        # Siempre que se muestre el panel administrativo,
        # ocupa toda la ventana.
        for widget in self.ventana.winfo_children():
            try:
                widget.destroy()
            except tk.TclError:
                pass

        self._pantalla_principal = None
        self._pantalla_actual = None
        self._callback_volver_actual = (
            self.volver_panel_principal
        )

        # =====================================================
        # CONTENEDOR CON SCROLL
        # =====================================================

        contenedor = VistaDesplazable(
            self.ventana,
            COLOR_FONDO,
        )

        contenedor.pack(
            fill="both",
            expand=True
        )

        self._pantalla_principal = contenedor
        self._pantalla_actual = contenedor

        contenido = contenedor.contenido

        # =====================================================
        # INTERIOR
        # =====================================================

        interior = tk.Frame(
            contenido,
            bg=COLOR_FONDO
        )

        interior.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=22
        )

        # =====================================================
        # DATOS DEL SISTEMA
        # =====================================================

        pacientes = self.sistema.obtener_pacientes()
        personal = self.sistema.obtener_personal()
        citas = self.sistema.obtener_citas()
        atenciones = self.sistema.obtener_atenciones()

        pendientes = [
            cita
            for cita in citas
            if cita.estado == "Pendiente"
        ]

        reprogramar = [
            cita
            for cita in citas
            if cita.estado == "Reprogramada"
        ]

        citas_atendidas = [
            cita
            for cita in citas
            if cita.estado == "Atendida"
        ]

        finalizadas = [
            atencion
            for atencion in atenciones
            if atencion.estado == "Finalizada"
        ]

        atenciones_proceso = [
            atencion
            for atencion in atenciones
            if atencion.estado == "En proceso"
        ]
        atenciones_no_atendidas = [
            atencion
            for atencion in atenciones
            if atencion.estado == "No atendida"
        ]

        def obtener_fecha_cita(cita):
            return cita.fecha_hora

        # =====================================================
        # PRÓXIMAS CITAS
        # =====================================================

        hoy = datetime.now()

        proximas = [
            cita
            for cita in citas
            if cita.estado in {"Pendiente", "Reprogramada", "En proceso"}
            and obtener_fecha_cita(cita) >= hoy
        ]

        proximas = sorted(
            proximas,
            key=obtener_fecha_cita
        )

        # =====================================================
        # ENCABEZADO / NAVEGACIÓN
        # =====================================================

        encabezado = tk.Frame(
            interior,
            bg=COLOR_FONDO
        )

        encabezado.pack(
            fill="x",
            pady=(0, 10)
        )

        izquierda = tk.Frame(
            encabezado,
            bg=COLOR_FONDO
        )

        izquierda.pack(
            side="left"
        )

        tk.Label(
            izquierda,
            text="ARCHINET",
            font=FUENTE_LOGO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(
            side="left"
        )

        tk.Label(
            izquierda,
            text=f"  |  PANEL ADMINISTRATIVO · {self.sesion.usuario}",
            font=FUENTE_NORMAL_BOLD,
            bg=COLOR_FONDO,
            fg=COLOR_GRIS_CLARO
        ).pack(
            side="left",
            pady=7
        )

        acciones = tk.Frame(
            encabezado,
            bg=COLOR_FONDO
        )

        acciones.pack(
            side="right"
        )

        boton_inicio = tk.Button(
            acciones,
            text="←  Volver",
            command=self.volver_a_inicio,
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

        boton_inicio.pack(
            side="left",
            padx=(0, 8)
        )

        boton_actualizar = tk.Button(
            acciones,
            text="↻  Actualizar",
            command=self.actualizar_dashboard,
            font=FUENTE_BOTON,
            bg=COLOR_ROJO,
            fg=COLOR_BLANCO,
            activebackground=COLOR_ROJO_CLARO,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=13,
            pady=8
        )

        boton_actualizar.pack(
            side="left"
        )

        for boton, color in (
            (
                boton_inicio,
                COLOR_PANEL_CLARO
            ),
            (
                boton_actualizar,
                COLOR_ROJO
            ),
        ):
            boton.bind(
                "<Enter>",
                lambda evento,
                b=boton,
                c=COLOR_ROJO_CLARO:
                b.configure(bg=c, fg=COLOR_BLANCO)
            )

            boton.bind(
                "<Leave>",
                lambda evento,
                b=boton,
                c=color:
                b.configure(
                    bg=c,
                    fg=(
                        COLOR_BLANCO
                        if c == COLOR_ROJO
                        else COLOR_TEXTO
                    ),
                )
            )

        tk.Frame(
            interior,
            bg=COLOR_ROJO,
            height=3
        ).pack(
            fill="x",
            pady=(0, 18)
        )

        # =====================================================
        # TÍTULO PRINCIPAL
        # =====================================================

        titulo_fila = tk.Frame(
            interior,
            bg=COLOR_FONDO
        )

        titulo_fila.pack(
            fill="x",
            pady=(0, 15)
        )

        titulo_info = tk.Frame(
            titulo_fila,
            bg=COLOR_FONDO
        )

        titulo_info.pack(
            side="left",
            fill="x",
            expand=True
        )

        tk.Label(
            titulo_info,
            text="Gestión integral de salud",
            font=FUENTE_TITULO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(
            anchor="w"
        )

        tk.Label(
            titulo_info,
            text=(
                ""
            ),
            font=FUENTE_SUBTITULO,
            bg=COLOR_FONDO,
            fg=COLOR_GRIS
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        self._crear_busqueda_rapida(interior)
        self._crear_resumen_dashboard(
            interior, pacientes, personal, citas, pendientes, reprogramar,
            citas_atendidas, atenciones, finalizadas, atenciones_proceso,
            atenciones_no_atendidas, proximas,
        )

