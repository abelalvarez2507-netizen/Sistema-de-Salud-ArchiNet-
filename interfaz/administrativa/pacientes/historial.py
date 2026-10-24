
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




class PacientesHistorialMixin:

    def historial_pacientes(self):
    
            pacientes = (
                self.sistema.obtener_pacientes()
            )
    
            if not pacientes:
    
                messagebox.showwarning(
                    "Aviso",
                    "No existen pacientes registrados."
                )
    
                return
    
            ventana = self._crear_pantalla_interna(
                "Historial de pacientes"
            )
    
            tk.Label(
                ventana,
                text="HISTORIAL DE PACIENTES",
                font=("Arial", 20, "bold")
            ).pack(
                pady=(15, 8)
            )
    
            tk.Label(
                ventana,
                text=(
                    "Consulte las citas y atenciones médicas "
                    "registradas del paciente."
                ),
                font=("Arial", 11)
            ).pack(
                pady=(0, 12)
            )
    
            # =====================================================
            # BÚSQUEDA DEL PACIENTE
            # =====================================================
    
            marco_busqueda = tk.Frame(
                ventana
            )
    
            marco_busqueda.pack(
                pady=5,
                padx=15
            )
    
            tk.Label(
                marco_busqueda,
                text="Buscar por:"
            ).grid(
                row=0,
                column=0,
                padx=5
            )
    
            tipo_var = tk.StringVar(
                value="Código"
            )
    
            tk.OptionMenu(
                marco_busqueda,
                tipo_var,
                "Código",
                "DNI"
            ).grid(
                row=0,
                column=1,
                padx=5
            )
    
            entrada_busqueda = tk.Entry(
                marco_busqueda,
                width=30
            )
    
            entrada_busqueda.grid(
                row=0,
                column=2,
                padx=5
            )
    
            self.configurar_limite_busqueda(
                entrada_busqueda,
                ventana
            )
    
            # =====================================================
            # ÁREA DE RESULTADOS CON SCROLL
            # =====================================================
    
            marco_resultado = tk.Frame(
                ventana
            )
    
            marco_resultado.pack(
                fill="both",
                expand=True,
                padx=15,
                pady=15
            )
    
            texto = tk.Text(
                marco_resultado,
                wrap="word",
                font=("Arial", 10),
                padx=10,
                pady=10
            )
    
            texto.pack(
                side="left",
                fill="both",
                expand=True
            )
    
            barra = tk.Scrollbar(
                marco_resultado,
                command=texto.yview
            )
    
            barra.pack(
                side="right",
                fill="y"
            )
    
            texto.config(
                yscrollcommand=barra.set
            )
    
            def mostrar_historial(*args):
    
                try:
    
                    tipo = tipo_var.get()
    
                    valor = (
                        entrada_busqueda
                        .get()
                        .strip()
                    )
    
                    if not valor:
    
                        raise ValueError(
                            "Ingrese el código o DNI del paciente."
                        )
    
                    paciente = None
    
                    if tipo == "Código":
    
                        resultados = (
                            self.sistema
                            .buscar_paciente_por_codigo(
                                valor
                            )
                        )
    
                    else:
    
                        dni = self.validar_dni(
                            valor
                        )
    
                        resultados = (
                            self.sistema
                            .buscar_paciente_por_dni(
                                dni
                            )
                        )
    
                    paciente = (
                        resultados[0]
                        if resultados
                        else None
                    )
    
                    if paciente is None:
    
                        raise ValueError(
                            "No se encontró el paciente."
                        )
    
                    texto.config(
                        state="normal"
                    )
    
                    texto.delete(
                        "1.0",
                        tk.END
                    )
    
                    # =================================================
                    # OBTENER REGISTROS
                    # =================================================
    
                    citas = [
                        cita
                        for cita
                        in self.sistema.obtener_citas()
                        if (
                            cita.paciente.codigo
                            == paciente.codigo
                        )
                    ]
    
                    atenciones = [
                        atencion
                        for atencion
                        in self.sistema.obtener_atenciones()
                        if (
                            atencion.paciente.codigo
                            == paciente.codigo
                        )
                    ]
                    ventas_medicamentos = self.sistema.obtener_historial_paciente(
                        paciente.codigo
                    ).get("ventas_medicamentos", [])
    
                    # =================================================
                    # DATOS DEL PACIENTE
                    # =================================================
    
                    texto.insert(
                        tk.END,
                        "==================================================\n"
                    )
    
                    texto.insert(
                        tk.END,
                        "              HISTORIAL DEL PACIENTE\n"
                    )
    
                    texto.insert(
                        tk.END,
                        "==================================================\n\n"
                    )
    
                    texto.insert(
                        tk.END,
                        "DATOS DEL PACIENTE\n"
                    )
    
                    texto.insert(
                        tk.END,
                        "--------------------------------------------------\n"
                    )
    
                    texto.insert(
                        tk.END,
                        f"Código: {paciente.codigo}\n"
                    )
    
                    texto.insert(
                        tk.END,
                        f"DNI: {paciente.dni}\n"
                    )
    
                    texto.insert(
                        tk.END,
                        f"Nombre: {paciente.nombre}\n"
                    )
    
                    texto.insert(
                        tk.END,
                        f"Edad: {paciente.edad} años\n\n"
                    )
    
                    # =================================================
                    # CITAS Y CONSULTAS
                    # =================================================
    
                    texto.insert(
                        tk.END,
                        "CITAS Y CONSULTAS DEL PACIENTE\n"
                    )
    
                    texto.insert(
                        tk.END,
                        "--------------------------------------------------\n"
                    )
    
                    if not citas:
    
                        texto.insert(
                            tk.END,
                            (
                                "El paciente no tiene "
                                "citas registradas.\n\n"
                            )
                        )
    
                    else:
    
                        for numero, cita in enumerate(
                            citas,
                            start=1
                        ):
    
                            texto.insert(
                                tk.END,
                                f"Consulta N.° {numero}\n"
                            )
    
                            texto.insert(
                                tk.END,
                                f"Código de cita: {cita.codigo}\n"
                            )
    
                            texto.insert(
                                tk.END,
                                f"Fecha y hora: {cita.fecha} {cita.hora}\n"
                            )
    
                            texto.insert(
                                tk.END,
                                (
                                    f"Profesional: "
                                    f"{cita.profesional.nombre}\n"
                                )
                            )
    
                            texto.insert(
                                tk.END,
                                (
                                    f"Código profesional: "
                                    f"{cita.profesional.codigo_profesional}\n"
                                )
                            )
    
                            texto.insert(
                                tk.END,
                                (
                                    f"Especialidad: "
                                    f"{cita.profesional.especialidad}\n"
                                )
                            )
    
                            texto.insert(
                                tk.END,
                                f"Motivo: {cita.motivo}\n"
                            )
    
                            texto.insert(
                                tk.END,
                                f"Estado: {cita.estado}\n"
                            )
    
                            texto.insert(
                                tk.END,
                                "--------------------------------------------------\n"
                            )
    
                    texto.insert(
                        tk.END,
                        "\n"
                    )
    
                    # =================================================
                    # ATENCIONES MÉDICAS
                    # =================================================
    
                    texto.insert(
                        tk.END,
                        "ATENCIONES MÉDICAS DEL PACIENTE\n"
                    )
    
                    texto.insert(
                        tk.END,
                        "--------------------------------------------------\n"
                    )
    
                    if not atenciones:
    
                        texto.insert(
                            tk.END,
                            (
                                "El paciente no tiene "
                                "atenciones registradas.\n"
                            )
                        )
    
                    else:
    
                        for numero, atencion in enumerate(
                            atenciones,
                            start=1
                        ):
    
                            texto.insert(
                                tk.END,
                                f"Atención N.° {numero}\n"
                            )
    
                            texto.insert(
                                tk.END,
                                (
                                    f"Código de atención: "
                                    f"{atencion.codigo}\n"
                                )
                            )
    
                            texto.insert(
                                tk.END,
                                (
                                    f"Cita relacionada: "
                                    f"{atencion.cita.codigo}\n"
                                )
                            )
    
                            texto.insert(
                                tk.END,
                                f"Fecha: {atencion.fecha}\n"
                            )
    
                            texto.insert(
                                tk.END,
                                (
                                    f"Profesional: "
                                    f"{atencion.profesional.nombre}\n"
                                )
                            )
    
                            texto.insert(
                                tk.END,
                                (
                                    f"Código profesional: "
                                    f"{atencion.profesional.codigo_profesional}\n"
                                )
                            )
    
                            texto.insert(
                                tk.END,
                                (
                                    f"Especialidad: "
                                    f"{atencion.profesional.especialidad}\n"
                                )
                            )
    
                            texto.insert(
                                tk.END,
                                (
                                    f"Diagnóstico: "
                                    f"{atencion.diagnostico}\n"
                                )
                            )
                            if atencion.informe_derivacion and atencion.informe_derivacion != atencion.diagnostico:
                                texto.insert(
                                    tk.END,
                                    f"Informe de derivación: {atencion.informe_derivacion}\n",
                                )
    
                            texto.insert(
                                tk.END,
                                f"Estado: {atencion.estado}\n"
                            )
                            if atencion.recetas:
                                texto.insert(tk.END, "Medicamentos recetados:\n")
                                for receta in atencion.recetas:
                                    texto.insert(tk.END, f"  • {receta.mostrar_informacion()}\n")
    
                            texto.insert(
                                tk.END,
                                "--------------------------------------------------\n"
                            )
    
                    texto.insert(tk.END, "\nMEDICAMENTOS REGISTRADOS EN VENTA\n")
                    texto.insert(tk.END, "--------------------------------------------------\n")
                    if not ventas_medicamentos:
                        texto.insert(tk.END, "No hay ventas de medicamentos vinculadas a este paciente.\n")
                    else:
                        for venta in ventas_medicamentos:
                            (_id, medicamento, lote, cantidad, _precio, total, codigo, vendedor, fecha_hora) = venta
                            texto.insert(
                                tk.END,
                                f"{fecha_hora} · {medicamento} · Lote {lote} · "
                                f"{cantidad} unidad(es) · S/ {float(total):.2f} · "
                                f"Paciente {codigo} · Registró: {vendedor}\n",
                            )
    
                    texto.insert(
                        tk.END,
                        "\nResumen: "
                        f"{len(citas)} cita(s) y "
                        f"{len(atenciones)} atención(es) registrada(s).\n"
                    )
    
                    texto.config(
                        state="disabled"
                    )
    
                    texto.see(
                        "1.0"
                    )
    
                except (
                    ValueError,
                    TypeError,
                    AttributeError
                ) as error:
    
                    texto.config(
                        state="normal"
                    )
    
                    texto.delete(
                        "1.0",
                        tk.END
                    )
    
                    texto.config(
                        state="disabled"
                    )
    
                    messagebox.showerror(
                        "Error",
                        str(error)
                    )
    
            def limpiar():
    
                entrada_busqueda.delete(
                    0,
                    tk.END
                )
    
                texto.config(
                    state="normal"
                )
    
                texto.delete(
                    "1.0",
                    tk.END
                )
    
                texto.config(
                    state="disabled"
                )
    
                entrada_busqueda.focus_set()
    
            # =====================================================
            # BOTONES DE CONSULTA
            # =====================================================
    
            tk.Button(
                marco_busqueda,
                text="Consultar historial",
                width=20,
                command=mostrar_historial
            ).grid(
                row=0,
                column=3,
                padx=8
            )
    
            tk.Button(
                marco_busqueda,
                text="Limpiar",
                width=12,
                command=limpiar
            ).grid(
                row=0,
                column=4,
                padx=5
            )
    
            entrada_busqueda.bind(
                "<Return>",
                mostrar_historial
            )
    
            entrada_busqueda.focus_set()
    
            texto.config(
                state="disabled"
            )
    def historial_clinico(self):
    
            self._callback_volver_actual = self.volver_panel_principal
    
            pacientes = (
                self.sistema.obtener_pacientes()
            )
    
            personal = (
                self.sistema.obtener_personal()
            )
    
            if not pacientes and not personal:
    
                messagebox.showwarning(
                    "Aviso",
                    (
                        "No existen pacientes ni "
                        "profesionales registrados."
                    )
                )
    
                return
    
            ventana = self._crear_pantalla_interna(
                "Historial clínico"
            )
    
            tk.Label(
                ventana,
                text="HISTORIAL CLÍNICO",
                font=("Arial", 22, "bold")
            ).pack(
                pady=30
            )
    
            tk.Label(
                ventana,
                text=(
                    "Seleccione qué historial desea consultar:"
                ),
                font=("Arial", 12)
            ).pack(
                pady=10
            )
    
            # =====================================================
            # BOTÓN PACIENTES
            # =====================================================
    
            tk.Button(
                ventana,
                text="PACIENTES",
                width=30,
                height=3,
                font=("Arial", 13, "bold"),
                command=lambda: self._abrir_desde_menu(
                    self.historial_pacientes,
                    self.historial_clinico,
                )
            ).pack(
                pady=15
            )
    
            # =====================================================
            # BOTÓN PROFESIONALES
            # =====================================================
    
            tk.Button(
                ventana,
                text="PROFESIONALES",
                width=30,
                height=3,
                font=("Arial", 13, "bold"),
                command=lambda: self._abrir_desde_menu(
                    self.historial_profesionales,
                    self.historial_clinico,
                )
            ).pack(
                pady=15
            )
    
            tk.Button(
                ventana,
                text="Cerrar",
                width=20,
                command=ventana.destroy
            ).pack(
                pady=20
            )

