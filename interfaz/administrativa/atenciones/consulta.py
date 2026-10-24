
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




class AtencionesConsultaMixin:

    def ver_atenciones(self):
    
            ventana = self._crear_pantalla_interna(
                "Atenciones médicas"
            )
    
            texto = tk.Text(
                ventana,
                width=105,
                height=25
            )
    
            texto.pack(
                padx=10,
                pady=10
            )
    
            atenciones = (
                self.sistema.obtener_atenciones()
            )
            codigos_con_atencion = {
                atencion.cita.codigo for atencion in atenciones
            }
            citas_en_seguimiento = [
                cita
                for cita in self.sistema.obtener_citas()
                if cita.codigo not in codigos_con_atencion
                and cita.estado in {"En proceso", "No atendida"}
            ]
    
            if not atenciones and not citas_en_seguimiento:
    
                texto.insert(
                    tk.END,
                    "No hay atenciones ni citas en proceso para mostrar."
                )
    
                texto.config(
                    state="disabled"
                )
    
                return
    
            texto.insert(
                tk.END,
                "ATENCIONES MÉDICAS\n"
            )
    
            texto.insert(
                tk.END,
                "========================================\n\n"
            )
    
            for atencion in atenciones:
    
                texto.insert(
                    tk.END,
                    atencion.mostrar_informacion()
                    + "\n\n"
                )
    
            for cita in citas_en_seguimiento:
                texto.insert(
                    tk.END,
                    (
                        f"Cita: {cita.codigo} | Paciente: {cita.paciente.nombre} | "
                        f"Profesional: {cita.profesional.nombre} | "
                        f"Fecha: {cita.fecha} {cita.hora} | "
                        f"Opinión pendiente | Estado: {cita.estado}\n\n"
                    )
                )
    
            texto.config(
                state="disabled"
            )

