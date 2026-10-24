
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




class PersonalHistorialMixin:

    def ver_historial_ventas_enfermeria(self):
            contenido = self._crear_pantalla_interna("Historial de ventas de enfermería")
            ventas = self.sistema.obtener_ventas_medicamentos(500)
            tk.Label(
                contenido,
                text=f"Últimas {len(ventas)} ventas registradas",
                font=FUENTE_SECCION,
                fg=COLOR_TEXTO,
                bg=COLOR_FONDO,
            ).pack(anchor="w", padx=24, pady=(18, 8))
    
            filtro = tk.StringVar(master=self.ventana)
            entrada = tk.Entry(
                contenido,
                textvariable=filtro,
                font=FUENTE_BOTON,
                bg=COLOR_PANEL_CLARO,
                fg=COLOR_TEXTO,
                relief="flat",
            )
            entrada.pack(fill="x", padx=24, pady=(0, 12), ipady=7)
            entrada.insert(0, "Buscar por paciente, medicamento o responsable")
            entrada.configure(fg=COLOR_GRIS)
    
            listado = tk.Frame(contenido, bg=COLOR_FONDO)
            listado.pack(fill="both", expand=True, padx=24, pady=(0, 20))
    
            def actualizar(*_args):
                for widget in listado.winfo_children():
                    widget.destroy()
                consulta = filtro.get().strip().casefold()
                if consulta == "buscar por paciente, medicamento o responsable":
                    consulta = ""
                resultados = [
                    venta
                    for venta in ventas
                    if not consulta
                    or consulta in " ".join(map(str, venta)).casefold()
                ]
                if not resultados:
                    tk.Label(
                        listado,
                        text="No hay ventas que coincidan con la búsqueda.",
                        font=FUENTE_BOTON,
                        fg=COLOR_GRIS,
                        bg=COLOR_FONDO,
                    ).pack(anchor="w", pady=12)
                    return
                for venta in resultados:
                    (_id, medicamento, lote, cantidad, precio, total, _cliente,
                     vendedor, fecha_hora, codigo_paciente) = venta
                    tarjeta = tk.Frame(
                        listado,
                        bg=COLOR_PANEL,
                        padx=16,
                        pady=12,
                        highlightthickness=1,
                        highlightbackground=COLOR_PANEL_CLARO,
                    )
                    tarjeta.pack(fill="x", pady=4)
                    tk.Label(
                        tarjeta,
                        text=f"{fecha_hora}   ·   {medicamento}   ·   Lote {lote}",
                        font=FUENTE_SECCION,
                        fg=COLOR_TEXTO,
                        bg=COLOR_PANEL,
                        wraplength=1050,
                        justify="left",
                    ).pack(anchor="w")
                    tk.Label(
                        tarjeta,
                        text=(
                            f"Paciente: {codigo_paciente or 'sin vincular'}   ·   "
                            f"Cantidad: {cantidad}   ·   "
                            f"Precio unitario: S/ {float(precio):.2f}   ·   "
                            f"Total: S/ {float(total):.2f}   ·   "
                            f"Registró: {vendedor}"
                        ),
                        font=FUENTE_BOTON,
                        fg=COLOR_GRIS,
                        bg=COLOR_PANEL,
                        wraplength=1050,
                        justify="left",
                    ).pack(anchor="w", pady=(5, 0))
    
            filtro.trace_add("write", actualizar)
            entrada.bind("<FocusIn>", lambda _evento: entrada.delete(0, tk.END))
            actualizar()
    def historial_profesionales(self):
    
            personal = [
                p for p in self.sistema.obtener_personal()
                if not self._es_personal_enfermeria(p)
            ]
    
            if not personal:
    
                messagebox.showwarning(
                    "Aviso",
                    "No existe personal profesional registrado."
                )
    
                return
    
            ventana = self._crear_pantalla_interna(
                "Historial de profesionales"
            )
    
            tk.Label(
                ventana,
                text="HISTORIAL DE PROFESIONALES",
                font=("Arial", 20, "bold")
            ).pack(
                pady=15
            )
    
            # =====================================================
            # BÚSQUEDA
            # =====================================================
    
            marco_busqueda = tk.Frame(
                ventana
            )
    
            marco_busqueda.pack(
                pady=5
            )
    
            tk.Label(
                marco_busqueda,
                text="Buscar profesional por:"
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
    
            texto = tk.Text(
                ventana,
                width=115,
                height=32
            )
    
            texto.pack(
                padx=10,
                pady=15
            )
    
            def mostrar_historial():
    
                try:
    
                    tipo = tipo_var.get()
    
                    valor = (
                        entrada_busqueda
                        .get()
                        .strip()
                    )
    
                    if not valor:
    
                        raise ValueError(
                            "Ingrese el código o DNI del profesional."
                        )
    
                    if tipo == "Código":
    
                        profesional = next(
                            (
                                p
                                for p in personal
                                if (
                                    p.codigo_profesional
                                    == valor
                                )
                            ),
                            None
                        )
    
                    else:
    
                        dni = self.validar_dni(
                            valor
                        )
    
                        profesional = next(
                            (
                                p
                                for p in personal
                                if p.dni == dni
                            ),
                            None
                        )
    
                    if profesional is None:
    
                        raise ValueError(
                            "No se encontró el profesional."
                        )
    
                    texto.config(
                        state="normal"
                    )
    
                    texto.delete(
                        "1.0",
                        tk.END
                    )
    
                    citas = [
                        cita
                        for cita
                        in self.sistema.obtener_citas()
                        if (
                            cita.profesional.codigo_profesional
                            == profesional.codigo_profesional
                        )
                    ]
    
                    atenciones = [
                        atencion
                        for atencion
                        in self.sistema.obtener_atenciones()
                        if (
                            atencion.cita.profesional.codigo_profesional
                            == profesional.codigo_profesional
                            or (
                                atencion.profesional_derivado
                                and atencion.profesional_derivado.codigo_profesional
                                == profesional.codigo_profesional
                            )
                        )
    
                    ]
    
                    # =================================================
                    # DATOS DEL PROFESIONAL
                    # =================================================
    
                    texto.insert(
                        tk.END,
                        "==================================================\n"
                    )
    
                    texto.insert(
                        tk.END,
                        "              HISTORIAL DEL PROFESIONAL\n"
                    )
    
                    texto.insert(
                        tk.END,
                        "==================================================\n\n"
                    )
    
                    texto.insert(
                        tk.END,
                        "DATOS DEL PROFESIONAL\n"
                    )
    
                    texto.insert(
                        tk.END,
                        "--------------------------------------------------\n"
                    )
    
                    texto.insert(
                        tk.END,
                        (
                            f"Código profesional: "
                            f"{profesional.codigo_profesional}\n"
                        )
                    )
    
                    texto.insert(
                        tk.END,
                        f"DNI: {profesional.dni}\n"
                    )
    
                    texto.insert(
                        tk.END,
                        f"Nombre: {profesional.nombre}\n"
                    )
    
                    texto.insert(
                        tk.END,
                        f"Edad: {profesional.edad} años\n"
                    )
    
                    texto.insert(
                        tk.END,
                        f"Especialidad: {profesional.especialidad}\n\n"
                    )
    
                    # =================================================
                    # CITAS
                    # =================================================
    
                    texto.insert(
                        tk.END,
                        "CITAS Y ACTIVIDADES DEL PROFESIONAL\n"
                    )
    
                    texto.insert(
                        tk.END,
                        "--------------------------------------------------\n"
                    )
    
                    if not citas:
    
                        texto.insert(
                            tk.END,
                            (
                                "El profesional no tiene "
                                "citas registradas.\n\n"
                            )
                        )
    
                    else:
    
                        for cita in citas:
    
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
                                    f"Paciente: "
                                    f"{cita.paciente.nombre}\n"
                                )
                            )
    
                            texto.insert(
                                tk.END,
                                (
                                    f"DNI del paciente: "
                                    f"{cita.paciente.dni}\n"
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
                    # ATENCIONES
                    # =================================================
    
                    texto.insert(
                        tk.END,
                        "ATENCIONES MÉDICAS REALIZADAS\n"
                    )
    
                    texto.insert(
                        tk.END,
                        "--------------------------------------------------\n"
                    )
    
                    if not atenciones:
    
                        texto.insert(
                            tk.END,
                            (
                                "El profesional no tiene "
                                "atenciones registradas.\n"
                            )
                        )
    
                    else:
    
                        for atencion in atenciones:
    
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
                                    f"Paciente: "
                                    f"{atencion.paciente.nombre}\n"
                                )
                            )
    
                            texto.insert(
                                tk.END,
                                (
                                    f"DNI del paciente: "
                                    f"{atencion.paciente.dni}\n"
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
    
                            texto.insert(
                                tk.END,
                                "--------------------------------------------------\n"
                            )
    
                    texto.config(
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
    
            tk.Button(
                marco_busqueda,
                text="Consultar historial",
                width=20,
                command=mostrar_historial
            ).grid(
                row=0,
                column=3,
                padx=10
            )

