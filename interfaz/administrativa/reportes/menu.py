
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




class ReportesMenuMixin:

    def gestion_reportes(self):
    
            self._crear_menu_gestion(
                "Reportes y estadísticas",
                (
                    "Consulte los principales indicadores "
                    "y reportes generados por Archinet."
                ),
                [
                    (
                        "Ver estadísticas",
                        self.ver_estadisticas
                    ),
                    (
                        "Ver reportes",
                        self.ver_reportes
                    ),
                ],
                ancho=520,
                alto=400
            )

