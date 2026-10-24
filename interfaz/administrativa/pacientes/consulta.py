
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




class PacientesConsultaMixin:

    def ver_pacientes(self):
    
            ventana = self._crear_pantalla_interna(
                "Pacientes registrados"
            )
    
            texto = tk.Text(
                ventana,
                width=90,
                height=23
            )
    
            texto.pack(
                padx=10,
                pady=10
            )
    
            pacientes = (
                self.sistema.obtener_pacientes()
            )
    
            if not pacientes:
    
                texto.insert(
                    tk.END,
                    "No existen pacientes registrados."
                )
    
                texto.config(
                    state="disabled"
                )
    
                return
    
            for paciente in pacientes:
    
                texto.insert(
                    tk.END,
                    paciente.mostrar_informacion()
                    + "\n\n"
                )
    
            texto.config(
                state="disabled"
            )
    def _mostrar_busqueda_personas(
            self,
            titulo,
            etiqueta,
            tipo_profesional=False,
            categoria_personal="profesional",
        ):
    
            self._limpiar_pantalla_actual()
    
            vista = VistaDesplazable(
                self.ventana,
                COLOR_FONDO,
            )
            vista.pack(fill="both", expand=True)
            ventana = vista.contenido
    
            self._pantalla_actual = vista
            instalar_navegacion(
                self.ventana,
                volver=(
                    self._callback_volver_actual
                    or self.volver_panel_principal
                ),
                inicio=self.volver_a_inicio,
            )
    
            contenedor = tk.Frame(
                ventana,
                bg=COLOR_FONDO
            )
    
            contenedor.pack(
                fill="both",
                expand=True,
                padx=35,
                pady=25
            )
    
            barra = tk.Frame(
                contenedor,
                bg=COLOR_FONDO
            )
    
            barra.pack(
                fill="x",
                pady=(0, 18)
            )
    
            boton_volver = tk.Button(
                barra,
                text="←  Volver",
                command=(
                    self._callback_volver_actual
                    or self.volver_panel_principal
                ),
                font=FUENTE_BOTON,
                bg=COLOR_PANEL_CLARO,
                fg=COLOR_TEXTO,
                activebackground=COLOR_ROJO,
                activeforeground=COLOR_BLANCO,
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=14,
                pady=8
            )
    
            boton_volver.pack(
                side="left"
            )
    
            tk.Label(
                contenedor,
                text=titulo,
                font=FUENTE_TITULO,
                bg=COLOR_FONDO,
                fg=COLOR_TEXTO
            ).pack(
                anchor="w",
                pady=(0, 4)
            )
    
            tk.Label(
                contenedor,
                text=etiqueta,
                font=FUENTE_NORMAL_BOLD,
                bg=COLOR_FONDO,
                fg=COLOR_GRIS_CLARO
            ).pack(
                anchor="w",
                pady=(0, 8)
            )
    
            tipo_var = tk.StringVar(
                value="Código"
            )
    
            fila_busqueda = tk.Frame(
                contenedor,
                bg=COLOR_FONDO
            )
    
            fila_busqueda.pack(
                fill="x",
                pady=(0, 15)
            )
    
            tk.OptionMenu(
                fila_busqueda,
                tipo_var,
                "Código",
                "DNI"
            ).pack(
                side="left",
                padx=(0, 10)
            )
    
            entrada_busqueda = tk.Entry(
                fila_busqueda,
                width=35,
                bg=COLOR_PANEL_CLARO,
                fg=COLOR_TEXTO,
                insertbackground=COLOR_TEXTO,
                relief="flat",
                bd=0,
                font=FUENTE_NORMAL
            )
    
            entrada_busqueda.pack(
                side="left",
                ipady=8
            )
    
            self.configurar_limite_busqueda(
                entrada_busqueda,
                self.ventana
            )
    
            boton_buscar = tk.Button(
                fila_busqueda,
                text="🔎  Buscar",
                command=lambda:
                buscar(),
                font=FUENTE_BOTON,
                bg=COLOR_ROJO,
                fg=COLOR_BLANCO,
                activebackground=COLOR_ROJO_CLARO,
                activeforeground=COLOR_BLANCO,
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=14,
                pady=7
            )
    
            boton_buscar.pack(
                side="left",
                padx=(10, 0)
            )
    
            resultado = tk.Text(
                contenedor,
                height=18,
                wrap="word",
                bg=COLOR_PANEL_CLARO,
                fg=COLOR_TEXTO,
                insertbackground=COLOR_TEXTO,
                relief="flat",
                bd=0,
                font=FUENTE_NORMAL
            )
    
            resultado.pack(
                fill="both",
                expand=True,
                pady=(5, 12)
            )
    
            def limpiar_entrada(*args):
    
                entrada_busqueda.delete(
                    0,
                    tk.END
                )
    
                resultado.config(
                    state="normal"
                )
    
                resultado.delete(
                    "1.0",
                    tk.END
                )
    
                resultado.config(
                    state="disabled"
                )
    
            tipo_var.trace_add(
                "write",
                limpiar_entrada
            )
    
            def buscar():
    
                try:
    
                    tipo = tipo_var.get()
    
                    valor = (
                        entrada_busqueda
                        .get()
                        .strip()
                    )
    
                    if not valor:
    
                        raise ValueError(
                            "Debe ingresar un valor "
                            "para realizar la búsqueda."
                        )
    
                    if tipo_profesional:
    
                        if tipo == "Código":
    
                            registros = (
                                self.sistema
                                .buscar_personal_por_codigo(
                                    valor
                                )
                            )
    
                        else:
    
                            registros = (
                                self.sistema
                                .buscar_personal_por_dni(
                                    self.validar_dni(
                                        valor
                                    )
                                )
                            )
    
                        registros = [
                            persona for persona in registros
                            if self._es_personal_enfermeria(persona)
                            == (categoria_personal == "enfermeria")
                        ]
                        mensaje_vacio = (
                            "No se encontró personal de enfermería."
                            if categoria_personal == "enfermeria"
                            else "No se encontró profesional."
                        )
    
                    else:
    
                        if tipo == "Código":
    
                            registros = (
                                self.sistema
                                .buscar_paciente_por_codigo(
                                    valor
                                )
                            )
    
                        else:
    
                            registros = (
                                self.sistema
                                .buscar_paciente_por_dni(
                                    self.validar_dni(
                                        valor
                                    )
                                )
                            )
    
                        mensaje_vacio = (
                            "No se encontraron pacientes."
                        )
    
                    resultado.config(
                        state="normal"
                    )
    
                    resultado.delete(
                        "1.0",
                        tk.END
                    )
    
                    if not registros:
    
                        resultado.insert(
                            tk.END,
                            mensaje_vacio
                        )
    
                        resultado.config(
                            state="disabled"
                        )
    
                        return
    
                    for registro in registros:
    
                        resultado.insert(
                            tk.END,
                            registro.mostrar_informacion()
                            + "\n\n"
                        )
    
                    resultado.config(
                        state="disabled"
                    )
    
                except (
                    ValueError,
                    TypeError
                ) as error:
    
                    messagebox.showerror(
                        "Error",
                        str(error)
                    )
    
            boton_buscar.configure(
                width=18
            )
    
            boton_buscar.bind(
                "<Enter>",
                lambda evento:
                boton_buscar.configure(
                    bg=COLOR_ROJO_CLARO
                )
            )
    
            boton_buscar.bind(
                "<Leave>",
                lambda evento:
                boton_buscar.configure(
                    bg=COLOR_ROJO
                )
            )
    
            entrada_busqueda.bind(
                "<Return>",
                lambda evento:
                buscar()
            )
    
            entrada_busqueda.focus_set()
    
            resultado.config(
                state="disabled"
            )

