import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from modelos.agenda.cita import Cita
from servicios.gestion.sistema_salud import SistemaSalud
from servicios.validacion import normalizar_fecha
from interfaz.campos import configurar_mascara_fecha
from servicios.validacion import validar_dni as validar_dni_valor

from interfaz.estilos import (
    COLOR_FONDO,
    COLOR_PANEL,
    COLOR_PANEL_CLARO,
    COLOR_ROJO,
    COLOR_ROJO_CLARO,
    COLOR_BLANCO,
    COLOR_ERROR,
    COLOR_TEXTO,
    COLOR_GRIS_CLARO,
    COLOR_GRIS,
    FUENTE_LOGO,
    FUENTE_TITULO,
    FUENTE_SUBTITULO,
    FUENTE_SECCION,
    FUENTE_BOTON
)
from interfaz.navegacion import VistaDesplazable, instalar_navegacion




class PacienteHistorialMixin:

    def mostrar_historial(self):

        if not self.paciente_autenticado():
            return

        paciente = self.paciente_actual

        try:

            historial = (
                self.sistema
                .obtener_historial_paciente(
                    paciente.codigo
                )
            )

        except ValueError as error:

            messagebox.showerror(
                "Historial",
                str(error)
            )

            return

        ventana = self._crear_pantalla_interna(
            "Mi historial clínico"
        )

        tk.Label(
            ventana,
            text=paciente.nombre,
            font=FUENTE_SUBTITULO,
            fg=COLOR_GRIS_CLARO,
            bg=COLOR_FONDO
        ).pack(
            pady=(0, 15)
        )

        marco_resultado = tk.Frame(
            ventana,
            bg=COLOR_FONDO
        )

        marco_resultado.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        texto = tk.Text(
            marco_resultado,
            width=82,
            height=20,
            font=("Arial", 10),
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="flat",
            bd=0,
            padx=15,
            pady=15
        )

        texto.pack(
            fill="both",
            expand=True
        )

        citas = historial["citas"]
        atenciones = historial["atenciones"]
        ventas_medicamentos = historial.get("ventas_medicamentos", [])

        texto.insert(
            tk.END,
            "=== CITAS ATENDIDAS ===\n\n"
        )

        if not citas:

            texto.insert(
                tk.END,
                "No existen citas atendidas registradas.\n\n"
            )

        else:

            for cita in citas:

                texto.insert(
                    tk.END,
                    f"Cita: {cita.codigo}\n"
                )

                texto.insert(
                    tk.END,
                    f"Fecha y hora: {cita.fecha} · {cita.hora}\n"
                )

                texto.insert(
                    tk.END,
                    f"Motivo: {cita.motivo}\n"
                )

                texto.insert(
                    tk.END,
                    (
                        "Profesional: "
                        f"{cita.profesional.nombre}\n"
                    )
                )

                texto.insert(
                    tk.END,
                    "\n"
                )

        texto.insert(
            tk.END,
            "=== ATENCIONES FINALIZADAS ===\n\n"
        )

        if not atenciones:

            texto.insert(
                tk.END,
                "No hay atenciones finalizadas ni derivaciones en curso.\n"
            )

        else:

            for atencion in atenciones:

                texto.insert(
                    tk.END,
                    f"Atención: {atencion.codigo}\n"
                )

                texto.insert(
                    tk.END,
                    f"Cita: {atencion.cita.codigo}\n"
                )

                texto.insert(
                    tk.END,
                    (
                        "Diagnóstico: "
                        f"{atencion.diagnostico}\n"
                    )
                )

                if (
                    atencion.informe_derivacion
                    and atencion.informe_derivacion != atencion.diagnostico
                ):
                    texto.insert(
                        tk.END,
                        f"Informe de derivación: {atencion.informe_derivacion}\n",
                    )

                if atencion.profesional_derivado:
                    texto.insert(
                        tk.END,
                        "Derivación: "
                        f"{atencion.profesional_derivado.nombre} · "
                        f"{atencion.profesional_derivado.especialidad}\n",
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
                    "\n"
                )

        texto.insert(tk.END, "=== MEDICAMENTOS REGISTRADOS EN VENTA ===\n\n")
        if not ventas_medicamentos:
            texto.insert(tk.END, "No hay medicamentos de venta vinculados a tu historial.\n")
        else:
            for venta in ventas_medicamentos:
                (_id, medicamento, lote, cantidad, _precio, total, codigo, vendedor, fecha_hora) = venta
                texto.insert(
                    tk.END,
                    f"{fecha_hora} · {medicamento} · Lote {lote} · "
                    f"{cantidad} unidad(es) · S/ {float(total):.2f} · "
                    f"Paciente {codigo}\n",
                )

        texto.configure(
            state="disabled"
        )

