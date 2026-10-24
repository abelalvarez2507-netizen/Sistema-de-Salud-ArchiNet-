
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




class ReportesInformesMixin:

    def ver_reportes(self):
    
            ventana = self._crear_pantalla_interna(
                "Reportes del sistema"
            )
    
            texto = tk.Text(
                ventana,
                width=100,
                height=35
            )
    
            texto.pack(
                padx=10,
                pady=10
            )
    
            reporte_pacientes = (
                self.reportes.reporte_pacientes()
            )
    
            reporte_profesionales = (
                self.reportes.reporte_profesionales()
            )
    
            reporte_citas = (
                self.reportes.reporte_citas()
            )
    
            reporte_atenciones = (
                self.reportes.reporte_atenciones()
            )
    
            reporte_general = (
                self.reportes.reporte_general()
            )
    
            # =====================================================
            # ENCABEZADO
            # =====================================================
    
            texto.insert(
                tk.END,
                "========================================\n"
            )
    
            texto.insert(
                tk.END,
                "             REPORTES ARCHINET\n"
            )
    
            texto.insert(
                tk.END,
                "========================================\n\n"
            )
    
            # =====================================================
            # GENERAL
            # =====================================================
    
            texto.insert(
                tk.END,
                "REPORTE GENERAL\n"
            )
    
            texto.insert(
                tk.END,
                "----------------------------------------\n"
            )
    
            texto.insert(
                tk.END,
                f"Pacientes: "
                f"{reporte_general['pacientes']}\n"
            )
    
            texto.insert(
                tk.END,
                f"Profesionales: "
                f"{reporte_general['profesionales']}\n"
            )
    
            texto.insert(
                tk.END,
                f"Citas: "
                f"{reporte_general['citas']}\n"
            )
    
            texto.insert(
                tk.END,
                f"Atenciones: "
                f"{reporte_general['atenciones']}\n\n"
            )
    
            # =====================================================
            # PACIENTES
            # =====================================================
    
            texto.insert(
                tk.END,
                "REPORTE DE PACIENTES\n"
            )
    
            texto.insert(
                tk.END,
                "----------------------------------------\n"
            )
    
            texto.insert(
                tk.END,
                f"Total: "
                f"{reporte_pacientes['total_pacientes']}\n"
            )
    
            texto.insert(
                tk.END,
                "Nombres registrados:\n"
            )
    
            for nombre in (
                reporte_pacientes["nombres"]
            ):
    
                texto.insert(
                    tk.END,
                    f"- {nombre}\n"
                )
    
            texto.insert(
                tk.END,
                "\n"
            )
    
            # =====================================================
            # PROFESIONALES
            # =====================================================
    
            texto.insert(
                tk.END,
                "REPORTE DE PROFESIONALES\n"
            )
    
            texto.insert(
                tk.END,
                "----------------------------------------\n"
            )
    
            texto.insert(
                tk.END,
                (
                    f"Total: "
                    f"{reporte_profesionales['total_profesionales']}\n"
                )
            )
    
            texto.insert(
                tk.END,
                "Especialidades:\n"
            )
    
            for especialidad in (
                reporte_profesionales["especialidades"]
            ):
    
                texto.insert(
                    tk.END,
                    f"- {especialidad}\n"
                )
    
            texto.insert(
                tk.END,
                "\n"
            )
    
            # =====================================================
            # CITAS
            # =====================================================
    
            texto.insert(
                tk.END,
                "REPORTE DE CITAS\n"
            )
    
            texto.insert(
                tk.END,
                "----------------------------------------\n"
            )
    
            texto.insert(
                tk.END,
                f"Total: "
                f"{reporte_citas['total_citas']}\n"
            )
    
            texto.insert(
                tk.END,
                f"Pendientes: "
                f"{reporte_citas['pendientes']}\n"
            )
    
            texto.insert(
                tk.END,
                f"Atendidas: "
                f"{reporte_citas['atendidas']}\n"
            )
    
            texto.insert(
                tk.END,
                f"Reprogramadas: "
                f"{reporte_citas['reprogramadas']}\n"
            )
    
            texto.insert(
                tk.END,
                f"No atendidas: "
                f"{reporte_citas['no_atendidas']}\n"
            )
    
            texto.insert(
                tk.END,
                f"Canceladas: "
                f"{reporte_citas['canceladas']}\n\n"
            )
    
            # =====================================================
            # ATENCIONES
            # =====================================================
    
            texto.insert(
                tk.END,
                "REPORTE DE ATENCIONES\n"
            )
    
            texto.insert(
                tk.END,
                "----------------------------------------\n"
            )
    
            texto.insert(
                tk.END,
                (
                    f"Total: "
                    f"{reporte_atenciones['total_atenciones']}\n"
                )
            )
    
            texto.insert(
                tk.END,
                (
                    f"Pendientes: "
                    f"{reporte_atenciones['pendientes']}\n"
                )
            )
    
            texto.insert(
                tk.END,
                (
                    f"En proceso: "
                    f"{reporte_atenciones['en_proceso']}\n"
                )
            )
    
            texto.insert(
                tk.END,
                (
                    f"Finalizadas: "
                    f"{reporte_atenciones['finalizadas']}\n\n"
                )
            )
    
            texto.insert(
                tk.END,
                "Diagnósticos registrados:\n"
            )
    
            for diagnostico in (
                reporte_atenciones["diagnosticos"]
            ):
    
                texto.insert(
                    tk.END,
                    f"- {diagnostico}\n"
                )
    
            texto.config(
                state="disabled"
            )

