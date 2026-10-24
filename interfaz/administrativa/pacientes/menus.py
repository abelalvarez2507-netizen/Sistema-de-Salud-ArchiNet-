
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




class PacientesMenusMixin:

    def gestion_pacientes(self):
    
            self._crear_menu_gestion(
                "Gestión de pacientes",
                "",
                [
                    (
                        "Registrar paciente",
                        self.registrar_paciente
                    ),
                    (
                        "Ver pacientes",
                        self.ver_pacientes
                    ),
                    (
                        "Buscar paciente",
                        self.buscar_paciente
                    ),
                    (
                        "Historial de pacientes",
                        self.historial_pacientes
                    ),
                ],
                ancho=520,
                alto=520
            )
    def buscar_paciente(self):
    
            self._mostrar_busqueda_personas(
                titulo="Buscar paciente",
                etiqueta="Buscar paciente por:",
                tipo_profesional=False
            )

