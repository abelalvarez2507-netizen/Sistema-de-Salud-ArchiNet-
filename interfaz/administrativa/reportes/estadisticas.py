
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




class ReportesEstadisticasMixin:

    def ver_estadisticas(self):
    
            ventana = self._crear_pantalla_interna(
                "Estadísticas del sistema"
            )
    
            reporte = (
                self.reportes.reporte_general()
            )
    
            reporte_citas = (
                self.reportes.reporte_citas()
            )
    
            reporte_atenciones = (
                self.reportes.reporte_atenciones()
            )
    
            estadisticas = [
                (
                    "Total de pacientes",
                    reporte["pacientes"]
                ),
                (
                    "Total de personal",
                    reporte["profesionales"]
                ),
                (
                    "Total de citas",
                    reporte["citas"]
                ),
                (
                    "Citas pendientes",
                    reporte_citas["pendientes"]
                ),
                (
                    "Citas atendidas",
                    reporte_citas["atendidas"]
                ),
                (
                    "Citas reprogramadas",
                    reporte_citas["reprogramadas"]
                ),
                (
                    "Citas no atendidas",
                    reporte_citas["no_atendidas"]
                ),
                (
                    "Citas canceladas",
                    reporte_citas["canceladas"]
                ),
                (
                    "Total de atenciones",
                    reporte["atenciones"]
                ),
                (
                    "Atenciones finalizadas",
                    reporte_atenciones["finalizadas"]
                ),
                (
                    "Atenciones en proceso",
                    reporte_atenciones["en_proceso"]
                )
            ]
    
            zona = tk.Frame(ventana, bg=COLOR_FONDO)
            zona.pack(fill="x", padx=25, pady=(8, 16))
            columnas_actuales = [0]
    
            def distribuir_estadisticas(evento=None):
                ancho = evento.width if evento is not None else zona.winfo_width()
                if ancho < 100:
                    return
    
                columnas = max(1, min(4, ancho // 280))
                if columnas == columnas_actuales[0]:
                    return
                columnas_actuales[0] = columnas
    
                for widget in zona.winfo_children():
                    widget.destroy()
    
                for columna in range(4):
                    zona.columnconfigure(
                        columna,
                        weight=1 if columna < columnas else 0,
                        uniform="estadisticas" if columna < columnas else "",
                    )
    
                for indice, (nombre, cantidad) in enumerate(estadisticas):
                    tarjeta = tk.Frame(
                        zona,
                        bg=COLOR_PANEL,
                        highlightbackground=COLOR_PANEL_CLARO,
                        highlightthickness=1,
                        padx=12,
                        pady=8,
                    )
                    tarjeta.grid(
                        row=indice // columnas,
                        column=indice % columnas,
                        sticky="nsew",
                        padx=5,
                        pady=5,
                    )
                    tk.Label(
                        tarjeta,
                        text=nombre,
                        font=("Arial", 10, "bold"),
                        fg=COLOR_GRIS_CLARO,
                        bg=COLOR_PANEL,
                        anchor="w",
                    ).pack(fill="x")
                    tk.Label(
                        tarjeta,
                        text=str(cantidad),
                        font=("Arial", 20, "bold"),
                        fg=COLOR_TEXTO,
                        bg=COLOR_PANEL,
                        anchor="w",
                    ).pack(fill="x", pady=(2, 0))
    
            zona.bind("<Configure>", distribuir_estadisticas)
            zona.after_idle(distribuir_estadisticas)

