
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




class AtencionesMenuMixin:

    def gestion_atenciones(self):
    
            self._crear_menu_gestion(
                "Atenciones médicas",
                "",
                [
                    (
                        "Registrar atención",
                        self.registrar_atencion
                    ),
                    (
                        "Ver atenciones",
                        self.ver_atenciones
                    ),
                    (
                        "Cambiar estado",
                        self.cambiar_estado_atencion
                    ),
                ],
                ancho=520,
                alto=460
            )

