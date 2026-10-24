
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




class AtencionesRegistroMixin:

    def registrar_atencion(self):
    
            citas = (
                self.sistema.obtener_citas()
            )
    
            if not citas:
    
                messagebox.showwarning(
                    "Aviso",
                    "Primero debe registrar una cita."
                )
    
                return
    
            citas_disponibles = [
                cita
                for cita in citas
                if not any(
                    atencion.cita.codigo
                    == cita.codigo
                    for atencion
                    in self.sistema.obtener_atenciones()
                )
                and cita.estado in {"Pendiente", "Reprogramada", "En proceso"}
            ]
    
            if not citas_disponibles:
    
                messagebox.showwarning(
                    "Aviso",
                    (
                        "No existen citas disponibles "
                        "para registrar una atención."
                    )
                )
    
                return
    
            ventana = self._crear_pantalla_interna(
                "Registrar atención"
            )
    
            codigo_generado = (
                self.sistema.generar_codigo_atencion()
            )
    
            tk.Label(
                ventana,
                text="Código de atención:"
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
                text="Cita:"
            ).pack(
                pady=5
            )
    
            cita_var = tk.StringVar()
    
            citas_texto = [
                (
                    f"{c.codigo} | "
                    f"{c.paciente.nombre} | "
                    f"{c.profesional.nombre} | "
                    f"{c.fecha} {c.hora}"
                )
                for c in citas_disponibles
            ]
    
            cita_var.set(
                citas_texto[0]
            )
    
            tk.OptionMenu(
                ventana,
                cita_var,
                *citas_texto
            ).pack()
    
            tk.Label(
                ventana,
                text="Diagnóstico:"
            ).pack(
                pady=5
            )
    
            entrada_diagnostico = tk.Entry(
                ventana,
                width=45
            )
    
            entrada_diagnostico.pack()
    
            tk.Label(
                ventana,
                text="Estado de la atención:"
            ).pack(
                pady=5
            )
    
            estado_var = tk.StringVar(
                value="Pendiente"
            )
    
            tk.OptionMenu(
                ventana,
                estado_var,
                "Pendiente",
                "En proceso",
                "Finalizada"
            ).pack()
    
            def guardar():
    
                try:
    
                    cita_codigo = (
                        cita_var
                        .get()
                        .split(" | ")[0]
                    )
    
                    cita = next(
                        c
                        for c in citas_disponibles
                        if c.codigo
                        == cita_codigo
                    )
    
                    atencion = AtencionMedica(
                        codigo_generado,
                        cita,
                        entrada_diagnostico.get(),
                        estado_var.get()
                    )
    
                    self.sistema.registrar_atencion(
                        atencion
                    )
    
                    messagebox.showinfo(
                        "Éxito",
                        (
                            "Atención registrada correctamente.\n\n"
                            f"Código: {codigo_generado}"
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
                text="Guardar atención",
                width=25,
                command=guardar
            ).pack(
                pady=25
            )

