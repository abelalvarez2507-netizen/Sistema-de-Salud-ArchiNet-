
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




class PersonalMenusMixin:

    def gestion_profesionales(self):
    
            self._crear_menu_gestion(
                "Gestión de profesionales",
                "",
                [
                    ("Registrar profesional", self.registrar_personal),
                    ("Ver profesionales", self.ver_personal),
                    ("Buscar profesional", self.buscar_personal),
                    ("Historial de profesionales", self.historial_profesionales),
                ],
                ancho=540,
                alto=520
            )
    def gestion_enfermeria(self):
            self._crear_menu_gestion(
                "Gestión de enfermería",
                "",
                [
                    ("Registrar personal", lambda: self.registrar_personal("enfermeria")),
                    ("Ver personal", lambda: self.ver_personal("enfermeria")),
                    ("Buscar personal", lambda: self.buscar_personal("enfermeria")),
                    ("Historial de ventas", self.ver_historial_ventas_enfermeria),
                ],
                ancho=540,
                alto=520,
            )

