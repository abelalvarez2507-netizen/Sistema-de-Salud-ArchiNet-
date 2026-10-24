
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




class PersonalConsultaMixin:

    def ver_personal(self, categoria="profesional"):
            personal_es_enfermeria = categoria == "enfermeria"
            ventana = self._crear_pantalla_interna(
                "Personal de enfermería" if personal_es_enfermeria else "Profesionales registrados"
            )
    
            texto = tk.Text(
                ventana,
                width=100,
                height=23
            )
    
            texto.pack(
                padx=10,
                pady=10
            )
    
            personal = [
                persona for persona in self.sistema.obtener_personal()
                if self._es_personal_enfermeria(persona) == personal_es_enfermeria
            ]
    
            if not personal:
    
                texto.insert(
                    tk.END,
                    "No existe personal registrado."
                )
    
                texto.config(
                    state="disabled"
                )
    
                return
    
            for profesional in personal:
    
                texto.insert(
                    tk.END,
                    profesional.mostrar_informacion()
                    + "\n\n"
                )
    
            texto.config(
                state="disabled"
            )
    def buscar_personal(self, categoria="profesional"):
            es_enfermeria = categoria == "enfermeria"
            self._mostrar_busqueda_personas(
                titulo="Buscar personal de enfermería" if es_enfermeria else "Buscar profesional",
                etiqueta="Buscar personal por:" if es_enfermeria else "Buscar profesional por:",
                tipo_profesional=True,
                categoria_personal=categoria,
            )

