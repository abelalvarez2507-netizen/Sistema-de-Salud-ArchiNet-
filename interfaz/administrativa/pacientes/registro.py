
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




class PacientesRegistroMixin:

    def registrar_paciente(self):
    
            ventana = self._crear_pantalla_interna(
                "Registrar paciente"
            )
    
            codigo_generado = (
                self.sistema.generar_codigo_paciente()
            )
    
            tk.Label(
                ventana,
                text="Código de paciente:"
            ).pack(
                pady=5
            )
    
            tk.Label(
                ventana,
                text=codigo_generado,
                font=("Arial", 14, "bold")
            ).pack(
                pady=5
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
    
            def guardar():
    
                try:
    
                    dni = self.validar_dni(
                        entrada_dni.get()
                    )
    
                    paciente = Paciente(
                        codigo_generado,
                        dni,
                        entrada_nombre.get(),
                        int(
                            entrada_edad.get()
                        )
                    )
    
                    self.sistema.registrar_paciente(
                        paciente
                    )
    
                    messagebox.showinfo(
                        "Éxito",
                        (
                            "Paciente registrado correctamente.\n\n"
                            f"Código asignado: "
                            f"{codigo_generado}\n"
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

