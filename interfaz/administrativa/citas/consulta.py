
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




class CitasConsultaMixin:

    def ver_citas(self):
    
            ventana = self._crear_pantalla_interna(
                "Citas pendientes"
            )
    
            texto = tk.Text(
                ventana,
                width=95,
                height=25
            )
    
            texto.pack(
                padx=10,
                pady=10
            )
    
            citas = (
                self.sistema
                .obtener_citas_pendientes()
            )
    
            if not citas:
    
                texto.insert(
                    tk.END,
                    "No existen citas pendientes."
                )
    
                texto.config(
                    state="disabled"
                )
    
                return
    
            texto.insert(
                tk.END,
                "CITAS PENDIENTES\n"
            )
    
            texto.insert(
                tk.END,
                "========================================\n\n"
            )
    
            for cita in citas:
    
                texto.insert(
                    tk.END,
                    cita.mostrar_informacion()
                    + "\n\n"
                )
    
            texto.config(
                state="disabled"
            )
    def ver_citas_reprogramadas(self):
    
            ventana = self._crear_pantalla_interna(
                "Citas reprogramadas"
            )
    
            texto = tk.Text(
                ventana,
                width=95,
                height=25
            )
    
            texto.pack(
                padx=10,
                pady=10
            )
    
            citas = (
                self.sistema
                .obtener_citas_reprogramadas()
            )
    
            if not citas:
    
                texto.insert(
                    tk.END,
                    "No existen citas reprogramadas."
                )
    
                texto.config(
                    state="disabled"
                )
    
                return
    
            texto.insert(
                tk.END,
                "CITAS PARA REPROGRAMAR\n"
            )
    
            texto.insert(
                tk.END,
                "========================================\n\n"
            )
    
            for cita in citas:
    
                texto.insert(
                    tk.END,
                    cita.mostrar_informacion()
                    + "\n\n"
                )
    
            texto.config(
                state="disabled"
            )

