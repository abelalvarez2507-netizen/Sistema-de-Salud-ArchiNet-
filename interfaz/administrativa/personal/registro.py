
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




class PersonalRegistroMixin:

    def registrar_personal(self, categoria="profesional"):
            es_enfermeria = categoria == "enfermeria"
            ventana = self._crear_pantalla_interna(
                "Registrar personal de enfermería" if es_enfermeria else "Registrar profesional"
            )
    
            codigo_generado = (
                self.generar_codigo_enfermeria()
                if es_enfermeria
                else self.generar_codigo_profesional()
            )
    
            tk.Label(
                ventana,
                text="DNI:"
            ).pack(
                pady=5
            )
    
            entrada_dni = tk.Entry(
                ventana,
                width=35
            )
    
            entrada_dni.pack()
    
            validacion = ventana.register(
                validar_dni_en_edicion
            )
    
            entrada_dni.config(
                validate="key",
                validatecommand=(
                    validacion,
                    "%P"
                )
            )
    
            tk.Label(
                ventana,
                text="Nombres y apellidos:"
            ).pack(
                pady=5
            )
    
            entrada_nombre = tk.Entry(
                ventana,
                width=35
            )
    
            entrada_nombre.pack()
            validar_nombre = ventana.register(validar_nombre_en_edicion)
            entrada_nombre.configure(
                validate="key",
                validatecommand=(validar_nombre, "%P"),
            )
    
            tk.Label(
                ventana,
                text="Edad:"
            ).pack(
                pady=5
            )
    
            entrada_edad = tk.Entry(
                ventana,
                width=35
            )
    
            entrada_edad.pack()
    
            tk.Label(
                ventana,
                text="Área de enfermería:" if es_enfermeria else "Especialidad:",
            ).pack(
                pady=5
            )
    
            especialidades = [
                "Medicina General",
                "Obstetricia",
                "Odontología",
                "Psicología",
                "Nutrición",
                "Medicina Familiar",
                "Urología",
                "Pediatría",
                "Neurología",
            ]
    
            especialidad_var = tk.StringVar(value="Enfermería" if es_enfermeria else especialidades[0])
            if not es_enfermeria:
                tk.OptionMenu(ventana, especialidad_var, *especialidades).pack()
    
            def guardar():
    
                try:
    
                    dni = self.validar_dni(
                        entrada_dni.get()
                    )
    
                    clase_personal = PersonalEnfermeria if es_enfermeria else PersonalSalud
                    profesional = clase_personal(
                        codigo_generado,
                        dni,
                        entrada_nombre.get(),
                        int(entrada_edad.get()),
                        especialidad_var.get(),
                    )
    
                    self.sistema.registrar_personal(profesional)
    
                    messagebox.showinfo(
                        "Éxito",
                        (
                            ("Personal de enfermería" if es_enfermeria else "Profesional")
                            + " registrado correctamente.\n\n"
                            f"Código asignado: {codigo_generado}\n"
                            "DNI almacenado de forma protegida."
                        )
                    )
    
                    ventana.destroy()
    
                except (
                    ValueError,
                    TypeError
                ) as error:
    
                    messagebox.showerror(
                        "Error",
                        str(error)
                    )
    
            tk.Button(
                ventana,
                text="Guardar",
                width=20,
                command=guardar
            ).pack(
                pady=20
            )

