
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


class AdministrativoResumenMixin:

    def _crear_resumen_dashboard(self, interior, pacientes, personal, citas, pendientes, reprogramar, citas_atendidas, atenciones, finalizadas, atenciones_proceso, atenciones_no_atendidas, proximas):
        # =====================================================
        # TARJETAS DE RESUMEN
        # =====================================================

        tk.Label(
            interior,
            text="RESUMEN DEL CENTRO",
            font=FUENTE_SECCION,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(
            anchor="w",
            pady=(0, 6)
        )

        resumen = tk.Frame(
            interior,
            bg=COLOR_FONDO
        )

        resumen.pack(
            fill="x",
            pady=(0, 15)
        )

        for columna in range(2):
            resumen.columnconfigure(
                columna,
                weight=1,
                uniform="resumen"
            )

        datos_resumen = [
            (
                "👥",
                "TOTAL DE PACIENTES",
                len(pacientes),
                "registrados"
            ),
            (
                "⚕",
                "TOTAL DE PROFESIONALES",
                len(personal),
                "registrados"
            ),
            (
                "📅",
                "CITAS PENDIENTES",
                len(pendientes),
                "por atender"
            ),
            (
                "🔄",
                "CITAS REPROGRAMADAS",
                len(reprogramar),
                "requieren seguimiento"
            ),
            (
                "🩺",
                "TOTAL DE ATENCIONES",
                len(atenciones),
                f"{len(finalizadas)} finalizadas"
            ),
            (
                "🕐",
                "PRÓXIMAS CITAS",
                len(proximas),
                "en la agenda"
            ),
        ]

        for indice, (
            icono,
            titulo,
            valor,
            detalle
        ) in enumerate(
            datos_resumen
        ):

            fila = indice // 2
            columna = indice % 2

            tarjeta = tk.Frame(
                resumen,
                bg=COLOR_PANEL,
                highlightbackground=COLOR_PANEL_CLARO,
                highlightthickness=1
            )

            tarjeta.grid(
                row=fila,
                column=columna,
                sticky="nsew",
                padx=5,
                pady=5
            )

            cabecera = tk.Frame(
                tarjeta,
                bg=COLOR_PANEL
            )

            cabecera.pack(
                fill="x",
                padx=14,
                pady=(11, 0)
            )

            tk.Label(
                cabecera,
                text=icono,
                font=("Arial", 19, "bold"),
                bg=COLOR_PANEL,
                fg=COLOR_ROJO
            ).pack(
                side="left"
            )

            tk.Label(
                cabecera,
                text=titulo,
                font=FUENTE_PEQUENA,
                bg=COLOR_PANEL,
                fg=COLOR_GRIS_CLARO,
                wraplength=210,
                justify="left"
            ).pack(
                side="left",
                padx=8
            )

            tk.Label(
                tarjeta,
                text=str(valor),
                font=("Arial", 25, "bold"),
                bg=COLOR_PANEL,
                fg=COLOR_TEXTO
            ).pack(
                anchor="w",
                padx=14,
                pady=(2, 0)
            )

            tk.Label(
                tarjeta,
                text=detalle,
                font=FUENTE_PEQUENA,
                bg=COLOR_PANEL,
                fg=COLOR_GRIS
            ).pack(
                anchor="w",
                padx=14,
                pady=(0, 11)
            )

        # =====================================================
        # AGENDA + ESTADO GENERAL
        # =====================================================

        centro = tk.Frame(
            interior,
            bg=COLOR_FONDO
        )

        centro.pack(
            fill="x",
            pady=(0, 16)
        )

        centro.columnconfigure(
            0,
            weight=3,
            uniform="centro"
        )

        centro.columnconfigure(
            1,
            weight=2,
            uniform="centro"
        )

        panel_citas = tk.Frame(
            centro,
            bg=COLOR_PANEL,
            highlightbackground=COLOR_PANEL_CLARO,
            highlightthickness=1
        )

        panel_citas.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 5)
        )

        tk.Label(
            panel_citas,
            text="PRÓXIMAS CITAS",
            font=FUENTE_SECCION,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO
        ).pack(
            anchor="w",
            padx=16,
            pady=(13, 2)
        )

        tk.Label(
            panel_citas,
            text="Vista rápida de la agenda registrada.",
            font=FUENTE_PEQUENA,
            bg=COLOR_PANEL,
            fg=COLOR_GRIS
        ).pack(
            anchor="w",
            padx=16,
            pady=(0, 9)
        )

        lista_citas = tk.Frame(
            panel_citas,
            bg=COLOR_PANEL
        )

        lista_citas.pack(
            fill="x",
            padx=16,
            pady=(0, 13)
        )

        if proximas:

            for cita in proximas[:6]:

                fila_cita = tk.Frame(
                    lista_citas,
                    bg=COLOR_PANEL_CLARO
                )

                fila_cita.pack(
                    fill="x",
                    pady=2
                )

                tk.Label(
                    fila_cita,
                    text=f"{cita.fecha} · {cita.hora}",
                    font=FUENTE_NORMAL_BOLD,
                    bg=COLOR_PANEL_CLARO,
                    fg=COLOR_ROJO_CLARO,
                    width=13,
                    anchor="w"
                ).pack(
                    side="left",
                    padx=10,
                    pady=7
                )

                nombre_paciente = getattr(
                    getattr(
                        cita,
                        "paciente",
                        None
                    ),
                    "nombre",
                    "Paciente"
                )

                nombre_profesional = getattr(
                    getattr(
                        cita,
                        "profesional",
                        None
                    ),
                    "nombre",
                    "Profesional"
                )

                datos = tk.Frame(
                    fila_cita,
                    bg=COLOR_PANEL_CLARO
                )

                datos.pack(
                    side="left",
                    fill="x",
                    expand=True,
                    padx=4,
                    pady=5
                )

                tk.Label(
                    datos,
                    text=str(nombre_paciente),
                    font=FUENTE_NORMAL_BOLD,
                    bg=COLOR_PANEL_CLARO,
                    fg=COLOR_TEXTO,
                    anchor="w"
                ).pack(
                    anchor="w"
                )

                tk.Label(
                    datos,
                    text=str(nombre_profesional),
                    font=FUENTE_PEQUENA,
                    bg=COLOR_PANEL_CLARO,
                    fg=COLOR_GRIS_CLARO,
                    anchor="w"
                ).pack(
                    anchor="w"
                )

                tk.Label(
                    fila_cita,
                    text=str(cita.estado),
                    font=FUENTE_PEQUENA,
                    bg=COLOR_PANEL_CLARO,
                    fg=COLOR_GRIS_CLARO,
                    width=14
                ).pack(
                    side="right",
                    padx=10
                )

        else:

            tk.Label(
                lista_citas,
                text="No hay citas futuras registradas.",
                font=FUENTE_NORMAL,
                bg=COLOR_PANEL,
                fg=COLOR_GRIS
            ).pack(
                anchor="w",
                pady=10
            )

        panel_estado = tk.Frame(
            centro,
            bg=COLOR_PANEL,
            highlightbackground=COLOR_PANEL_CLARO,
            highlightthickness=1
        )

        panel_estado.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 0)
        )

        tk.Label(
            panel_estado,
            text="📊 ESTADO DEL CENTRO",
            font=FUENTE_SECCION,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO
        ).pack(
            anchor="w",
            padx=16,
            pady=(13, 10)
        )

        estado_resumen = [
            (
                "Pacientes registrados",
                len(pacientes)
            ),
            (
                "Profesionales registrados",
                sum(not self._es_personal_enfermeria(p) for p in personal)
            ),
            (
                "Personal de enfermería",
                sum(self._es_personal_enfermeria(p) for p in personal)
            ),
            (
                "Citas registradas",
                len(citas)
            ),
            (
                "Citas pendientes",
                len(pendientes)
            ),
            (
                "Citas atendidas",
                len(citas_atendidas)
            ),
            (
                "Citas en proceso",
                sum(cita.estado == "En proceso" for cita in citas)
            ),
            (
                "Citas reprogramadas",
                len(reprogramar)
            ),
                (
                    "Citas no atendidas",
                    sum(cita.estado == "No atendida" for cita in citas)
                ),
                (
                    "Citas canceladas",
                    sum(cita.estado == "Cancelada" for cita in citas)
                ),
            (
                "Atenciones en proceso",
                len(atenciones_proceso)
            ),
            (
                "Atenciones no atendidas",
                len(atenciones_no_atendidas)
            ),
            (
                "Atenciones finalizadas",
                len(finalizadas)
            ),
        ]

        for nombre, cantidad in estado_resumen:

            fila_estado = tk.Frame(
                panel_estado,
                bg=COLOR_PANEL
            )

            fila_estado.pack(
                fill="x",
                padx=16,
                pady=3
            )

            tk.Label(
                fila_estado,
                text=nombre,
                font=FUENTE_PEQUENA,
                bg=COLOR_PANEL,
                fg=COLOR_GRIS_CLARO
            ).pack(
                side="left"
            )

            tk.Label(
                fila_estado,
                text=str(cantidad),
                font=FUENTE_NORMAL_BOLD,
                bg=COLOR_PANEL,
                fg=COLOR_TEXTO
            ).pack(
                side="right"
            )

        aviso = (
            "Hay citas pendientes de atención."
            if pendientes
            else "No hay citas pendientes actualmente."
        )

        tk.Label(
            panel_estado,
            text=aviso,
            font=FUENTE_PEQUENA,
            bg=COLOR_PANEL,
            fg=COLOR_GRIS,
            wraplength=330,
            justify="left"
        ).pack(
            anchor="w",
            padx=16,
            pady=(9, 13)
        )

        # =====================================================
        # MÓDULOS PRINCIPALES
        # =====================================================

        tk.Label(
            interior,
            text="MÓDULOS DEL SISTEMA",
            font=FUENTE_SECCION,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(
            anchor="w",
            pady=(0, 6)
        )

        zona = tk.Frame(
            interior,
            bg=COLOR_FONDO
        )

        zona.pack(
            fill="x",
            pady=(0, 12)
        )

        for columna in range(3):
            zona.columnconfigure(
                columna,
                weight=1,
                uniform="modulos"
            )


        self._crear_modulo(zona, 
            0,
            0,
            "👥",
            "GESTIÓN DE PACIENTES",
            "",
            len(pacientes),
            "pacientes registrados",
            "Gestionar pacientes",
            self.gestion_pacientes
        )

        self._crear_modulo(zona, 
            0,
            1,
            "⚕",
            "GESTIÓN DE PROFESIONALES",
            "",
            sum(not self._es_personal_enfermeria(p) for p in personal),
            "profesionales registrados",
            "Gestionar profesionales",
            self.gestion_profesionales
        )

        self._crear_modulo(zona, 
            1,
            0,
            "📅",
            "GESTIÓN DE CITAS",
            "",
            len(citas),
            "citas en agenda",
            "Gestionar citas",
            self.gestion_citas
        )

        self._crear_modulo(zona, 
            0,
            2,
            "♧",
            "GESTIÓN DE ENFERMERÍA",
            "",
            sum(self._es_personal_enfermeria(p) for p in personal),
            "personas registradas",
            "Gestionar enfermería",
            self.gestion_enfermeria
        )

        self._crear_modulo(zona, 
            1,
            1,
            "🩺",
            "ATENCIONES MÉDICAS",
            "",
            len(atenciones),
            "atenciones registradas",
            "Gestionar atenciones",
            self.gestion_atenciones
        )

        self._crear_modulo(zona, 
            1,
            2,
            "📊",
            "REPORTES Y ESTADÍSTICAS",
            "",
            len(finalizadas),
            "atenciones finalizadas",
            "Ver reportes",
            self.gestion_reportes
        )

        # =====================================================
        # PIE DEL PANEL
        # =====================================================

        pie = tk.Frame(
            interior,
            bg=COLOR_FONDO
        )

        pie.pack(
            fill="x",
            pady=(5, 8)
        )

        tk.Frame(
            pie,
            bg=COLOR_PANEL_CLARO,
            height=1
        ).pack(
            fill="x",
            pady=(0, 9)
        )

        tk.Label(
            pie,
            text=(
                "Archinet • Sistema de Salud Rural • "
                "Panel administrativo"
            ),
            font=FUENTE_PEQUENA,
            bg=COLOR_FONDO,
            fg=COLOR_GRIS_OSCURO
        ).pack(
            side="left"
        )

