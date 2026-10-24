
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




class CitasAgendaMixin:

    def reprogramar_cita(self):
            self.sistema.actualizar_citas_vencidas()
            citas = [
                cita
                for cita in self.sistema.obtener_citas()
                if cita.estado in {"Pendiente", "Reprogramada"}
            ]
            if not citas:
                messagebox.showinfo(
                    "Reprogramar cita",
                    "No hay citas pendientes que se puedan reprogramar.",
                )
                return
    
            ventana = self._crear_pantalla_interna("Reprogramar una cita")
            tk.Label(ventana, text="Selecciona la cita:").pack(pady=(8, 4))
            cita_var = tk.StringVar()
            opciones = [
                f"{cita.codigo} | {cita.paciente.nombre} | {cita.fecha} {cita.hora}"
                for cita in citas
            ]
            cita_var.set(opciones[0])
            tk.OptionMenu(ventana, cita_var, *opciones).pack()
            tk.Label(ventana, text="Nueva fecha:").pack(pady=(12, 2))
            entrada_fecha = self.crear_campo_fecha(ventana)
    
            profesional_var = tk.StringVar()
            hora_var, actualizar = self.crear_selector_horarios(
                ventana,
                profesional_var,
                entrada_fecha,
            )
    
            def cita_seleccionada(*_args):
                codigo = cita_var.get().split(" | ")[0]
                cita = next(item for item in citas if item.codigo == codigo)
                profesional_var.set(
                    f"{cita.profesional.codigo_profesional} - {cita.profesional.nombre}"
                )
    
            cita_var.trace_add("write", cita_seleccionada)
            cita_seleccionada()
    
            tk.Button(
                ventana,
                text="Ver horarios disponibles",
                command=actualizar,
                cursor="hand2",
            ).pack(pady=(6, 10))
    
            def guardar():
                try:
                    if entrada_fecha.placeholder_activo:
                        raise ValueError("Ingresa la nueva fecha de la cita.")
                    if not hora_var.get():
                        raise ValueError("Selecciona un horario disponible.")
                    codigo = cita_var.get().split(" | ")[0]
                    self.sistema.reprogramar_cita(
                        codigo,
                        entrada_fecha.get(),
                        hora_var.get(),
                    )
                    messagebox.showinfo(
                        "Cita reprogramada",
                        "La cita se guardó con la nueva fecha y horario.",
                    )
                    ventana.destroy()
                except (ValueError, StopIteration) as error:
                    messagebox.showerror(
                        "No se pudo reprogramar",
                        str(error),
                        parent=ventana,
                    )
    
            tk.Button(
                ventana,
                text="Guardar nueva fecha",
                width=24,
                command=guardar,
                cursor="hand2",
            ).pack(pady=12)
    def cancelar_cita(self):
            self.sistema.actualizar_citas_vencidas()
            citas = [
                cita
                for cita in self.sistema.obtener_citas()
                if cita.estado in {"Pendiente", "Reprogramada"}
            ]
            if not citas:
                messagebox.showinfo(
                    "Cancelar cita",
                    "No hay citas pendientes que se puedan cancelar.",
                )
                return
    
            ventana = self._crear_pantalla_interna("Cancelar una cita")
            tk.Label(ventana, text="Selecciona la cita que deseas cancelar:").pack(pady=(8, 4))
            cita_var = tk.StringVar()
            opciones = [
                f"{cita.codigo} | {cita.paciente.nombre} | {cita.fecha} {cita.hora}"
                for cita in citas
            ]
            cita_var.set(opciones[0])
            tk.OptionMenu(ventana, cita_var, *opciones).pack()
    
            def cancelar():
                codigo = cita_var.get().split(" | ")[0]
                cita = next(item for item in citas if item.codigo == codigo)
                if not messagebox.askyesno(
                    "Confirmar cancelación",
                    f"¿Cancelar la cita de {cita.paciente.nombre} del {cita.fecha} a las {cita.hora}?",
                    parent=ventana,
                ):
                    return
                try:
                    self.sistema.cancelar_cita(codigo)
                    messagebox.showinfo(
                        "Cita cancelada",
                        "La cita se canceló correctamente.",
                        parent=ventana,
                    )
                    ventana.destroy()
                except ValueError as error:
                    messagebox.showerror(
                        "No se pudo cancelar",
                        str(error),
                        parent=ventana,
                    )
    
            tk.Button(
                ventana,
                text="Cancelar cita seleccionada",
                width=28,
                command=cancelar,
                cursor="hand2",
            ).pack(pady=18)

