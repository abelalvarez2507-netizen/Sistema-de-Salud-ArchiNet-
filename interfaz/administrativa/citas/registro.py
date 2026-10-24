
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




class CitasRegistroMixin:

    def registrar_cita(self):
    
            pacientes = (
                self.sistema.obtener_pacientes()
            )
    
            personal = (
                self.sistema.obtener_personal()
            )
    
            if not pacientes:
    
                messagebox.showwarning(
                    "Aviso",
                    "Primero debe registrar un paciente."
                )
    
                return
    
            if not personal:
    
                messagebox.showwarning(
                    "Aviso",
                    "Primero debe registrar personal de salud."
                )
    
                return
    
            ventana = self._crear_pantalla_interna(
                "Registrar cita"
            )
    
            codigo_generado = (
                self.sistema.generar_codigo_cita()
            )
    
            tk.Label(
                ventana,
                text="Código de cita:"
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
                text="Paciente:"
            ).pack(
                pady=5
            )
    
            paciente_var = tk.StringVar()
    
            pacientes_texto = [
                f"{p.codigo} - {p.nombre}"
                for p in pacientes
            ]
    
            paciente_var.set(
                pacientes_texto[0]
            )
    
            tk.OptionMenu(
                ventana,
                paciente_var,
                *pacientes_texto
            ).pack()
    
            tk.Label(
                ventana,
                text="Profesional:"
            ).pack(
                pady=5
            )
    
            profesional_var = tk.StringVar()
    
            personal_texto = [
                (
                    f"{p.codigo_profesional} - "
                    f"{p.nombre} - "
                    f"{p.especialidad}"
                )
                for p in personal
            ]
    
            profesional_var.set(
                personal_texto[0]
            )
    
            tk.OptionMenu(
                ventana,
                profesional_var,
                *personal_texto
            ).pack()
    
            tk.Label(
                ventana,
                text="Fecha:"
            ).pack(
                pady=5
            )
    
            entrada_fecha = (
                self.crear_campo_fecha(
                    ventana
                )
            )
    
            hora_var, actualizar_horarios = self.crear_selector_horarios(
                ventana,
                profesional_var,
                entrada_fecha,
            )
    
            tk.Button(
                ventana,
                text="Ver horarios disponibles",
                command=actualizar_horarios,
                cursor="hand2",
            ).pack(pady=(5, 8))
    
            tk.Label(
                ventana,
                text="Motivo:"
            ).pack(
                pady=5
            )
    
            entrada_motivo = tk.Entry(
                ventana,
                width=40
            )
    
            entrada_motivo.pack()
    
            def guardar():
    
                try:
    
                    if entrada_fecha.placeholder_activo:
    
                        raise ValueError(
                            "Debe ingresar una fecha."
                        )
    
                    fecha = (
                        entrada_fecha.get()
                    )
    
                    self.validar_fecha(
                        fecha
                    )
    
                    if not hora_var.get():
                        raise ValueError(
                            "Selecciona un horario disponible para esta cita."
                        )
    
                    paciente_codigo = (
                        paciente_var
                        .get()
                        .split(" - ")[0]
                    )
    
                    profesional_codigo = (
                        profesional_var
                        .get()
                        .split(" - ")[0]
                    )
    
                    paciente = next(
                        p
                        for p in pacientes
                        if p.codigo
                        == paciente_codigo
                    )
    
                    profesional = next(
                        p
                        for p in personal
                        if (
                            p.codigo_profesional
                            == profesional_codigo
                        )
                    )
    
                    cita = Cita(
                        codigo_generado,
                        paciente,
                        profesional,
                        fecha,
                        entrada_motivo.get(),
                        "Pendiente",
                        hora_var.get(),
                    )
    
                    self.sistema.registrar_cita(
                        cita
                    )
    
                    messagebox.showinfo(
                        "Éxito",
                        (
                            "Cita registrada correctamente.\n\n"
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
                text="Guardar cita",
                width=25,
                command=guardar
            ).pack(
                pady=25
            )

