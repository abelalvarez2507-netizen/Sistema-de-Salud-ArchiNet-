
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




class AtencionesSeguimientoMixin:

    def cambiar_estado_atencion(self):
    
            self.sistema.actualizar_citas_vencidas()
    
            atenciones = [
                atencion
                for atencion
                in self.sistema.obtener_atenciones()
                if atencion.estado not in {"Finalizada", "No atendida"}
            ]
    
            if not atenciones:
    
                messagebox.showwarning(
                    "Aviso",
                    (
                        "No existen atenciones disponibles "
                        "para cambiar de estado."
                    )
                )
    
                return
    
            ventana = self._crear_pantalla_interna(
                "Cambiar estado de atención"
            )
    
            tk.Label(
                ventana,
                text="Seleccione la atención:"
            ).pack(
                pady=10
            )
    
            atencion_var = tk.StringVar()
    
            atenciones_texto = [
                (
                    f"{a.codigo} | "
                    f"{a.paciente.nombre} | "
                    f"{a.profesional.nombre} | "
                    f"{a.estado}"
                )
                for a in atenciones
            ]
    
            atencion_var.set(
                atenciones_texto[0]
            )
    
            tk.OptionMenu(
                ventana,
                atencion_var,
                *atenciones_texto
            ).pack()
    
            tk.Label(
                ventana,
                text="Nuevo estado de la atención:"
            ).pack(
                pady=15
            )
    
            estado_var = tk.StringVar()
    
            tk.OptionMenu(
                ventana,
                estado_var,
                "Pendiente",
                "En proceso",
                "Finalizada",
                "No atendida",
            ).pack()
    
            informacion = tk.Label(
                ventana,
                text="",
                justify="left"
            )
    
            informacion.pack(
                pady=20
            )
    
            def mostrar_informacion(*args):
    
                try:
    
                    codigo = (
                        atencion_var
                        .get()
                        .split(" | ")[0]
                    )
    
                    atencion = next(
                        a
                        for a in atenciones
                        if a.codigo == codigo
                    )
    
                    informacion.config(
                        text=(
                            f"Paciente: "
                            f"{atencion.paciente.nombre}\n"
                            f"Profesional: "
                            f"{atencion.profesional.nombre}\n"
                            f"Fecha: {atencion.fecha}\n"
                            f"Diagnóstico: "
                            f"{atencion.diagnostico}\n"
                            f"Estado actual: "
                            f"{atencion.estado}"
                        )
                    )
    
                    # Ahora el selector comienza con el estado real.
                    estado_var.set(
                        atencion.estado
                    )
    
                except (
                    ValueError,
                    StopIteration
                ):
                    pass
    
            atencion_var.trace_add(
                "write",
                mostrar_informacion
            )
    
            mostrar_informacion()
    
            def actualizar():
    
                try:
    
                    codigo_atencion = (
                        atencion_var
                        .get()
                        .split(" | ")[0]
                    )
    
                    nuevo_estado = (
                        estado_var.get()
                    )
    
                    self.sistema.actualizar_estado_atencion(
                        codigo_atencion,
                        nuevo_estado
                    )
    
                    if nuevo_estado == "Finalizada":
    
                        mensaje = (
                            "La atención fue finalizada.\n\n"
                            "La cita también quedó marcada como atendida.\n"
                            "El registro NO fue eliminado.\n"
                            "Ahora aparecerá en el "
                            "Historial Clínico y ya no "
                            "aparecerá en este selector."
                        )
    
                    elif nuevo_estado == "En proceso":
    
                        mensaje = (
                            "La atención y la cita quedaron en proceso."
                        )
    
                    elif nuevo_estado == "No atendida":
    
                        mensaje = (
                            "La atención y la cita quedaron marcadas como no atendidas."
                        )
    
                    else:
    
                        mensaje = (
                            "La atención y la cita volvieron a estar pendientes."
                        )
    
                    messagebox.showinfo(
                        "Estado actualizado",
                        mensaje
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
                text="Actualizar estado",
                width=25,
                command=actualizar
            ).pack(
                pady=20
            )

