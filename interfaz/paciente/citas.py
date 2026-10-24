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




class PacienteCitasMixin:

    def solicitar_cita(self):
        if not self.paciente_autenticado():
            return

        medicos = [
            profesional
            for profesional in self.sistema.obtener_personal()
            if "enfermer" not in profesional.especialidad.casefold()
        ]
        if not medicos:
            messagebox.showwarning(
                "Sin profesionales",
                "Todavía no hay médicos registrados para reservar una cita.",
            )
            return

        pantalla = self._crear_pantalla_interna("Solicitar una cita")
        tk.Label(
            pantalla,
            text=f"Paciente: {self.paciente_actual.nombre}",
            font=FUENTE_SUBTITULO,
            fg=COLOR_GRIS_CLARO,
            bg=COLOR_FONDO,
        ).pack(pady=(0, 12))

        formulario = tk.Frame(pantalla, bg=COLOR_PANEL, padx=24, pady=18)
        formulario.pack(fill="x", padx=60, pady=10)

        tk.Label(
            formulario,
            text="Atención médica general",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            font=FUENTE_BOTON,
        ).pack(anchor="w")

        tk.Label(formulario, text="Fecha (DD/MM/AAAA):", bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(anchor="w")
        entrada_fecha = tk.Entry(
            formulario,
            width=20,
            justify="center",
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="flat",
        )
        entrada_fecha.pack(anchor="w", pady=(4, 12), ipady=6)
        configurar_mascara_fecha(entrada_fecha)

        tk.Label(
            formulario,
            text="Horarios disponibles (turnos de 30 minutos):",
            font=FUENTE_BOTON,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        ).pack(anchor="w")
        tk.Label(
            formulario,
            text="Atención de 07:00 a 18:00",
            font=("Arial", 9),
            bg=COLOR_PANEL,
            fg=COLOR_GRIS,
        ).pack(anchor="w", pady=(2, 6))

        hora_var = tk.StringVar(value="")
        menu_hora = tk.OptionMenu(formulario, hora_var, "")
        menu_hora.configure(bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO, relief="flat")
        menu_hora.pack(anchor="w", pady=(0, 12))

        def actualizar_horarios(event=None):
            try:
                fecha = normalizar_fecha(entrada_fecha.get())
                horarios = self.sistema.horarios_disponibles_para_cita(
                    fecha,
                    paciente_codigo=self.paciente_actual.codigo,
                )
            except ValueError:
                horarios = []
            menu = menu_hora["menu"]
            menu.delete(0, "end")
            if horarios:
                for hora in horarios:
                    menu.add_command(
                        label=hora,
                        command=lambda valor=hora: hora_var.set(valor),
                    )
                hora_var.set(horarios[0])
            else:
                menu.add_command(
                    label="Ingrese una fecha valida",
                    command=lambda: None,
                )
                hora_var.set("")

        self._boton_cita = tk.Button(
            formulario,
            text="Ver horarios disponibles",
            command=actualizar_horarios,
            font=FUENTE_BOTON,
            bg=COLOR_ROJO,
            fg=COLOR_BLANCO,
            activebackground=COLOR_ROJO_CLARO,
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6,
        )
        self._boton_cita.pack(anchor="w", pady=(0, 12))
        entrada_fecha.bind("<FocusOut>", actualizar_horarios)
        entrada_fecha.bind("<Return>", actualizar_horarios)

        tk.Label(formulario, text="Motivo de la cita:", bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(anchor="w")
        entrada_motivo = tk.Entry(
            formulario,
            width=55,
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="flat",
        )
        entrada_motivo.pack(anchor="w", pady=(4, 8), ipady=6)

        def guardar():
            try:
                fecha = normalizar_fecha(entrada_fecha.get())
                if not hora_var.get():
                    raise ValueError("Selecciona un horario disponible.")
                cita = self.sistema.crear_cita_asignacion_automatica(
                    self.paciente_actual,
                    fecha,
                    entrada_motivo.get(),
                    hora_var.get(),
                )
            except ValueError as error:
                messagebox.showerror("No se pudo registrar la cita", str(error))
                return

            try:
                self._sincronizar_datos_privados()
            except (OSError, ValueError) as error:
                messagebox.showwarning(
                    "Cita registrada",
                    "La cita quedó guardada, pero no se pudo actualizar el archivo privado: " + str(error),
                )
            else:
                messagebox.showinfo(
                    "Cita solicitada",
                    f"Tu cita quedó registrada para el {cita.fecha} a las {cita.hora} con {cita.profesional.nombre} ({cita.profesional.especialidad}).",
                )
            self.crear_interfaz()

        tk.Button(
            formulario,
            text="Confirmar cita",
            command=guardar,
            font=FUENTE_BOTON,
            bg=COLOR_ROJO,
            fg=COLOR_BLANCO,
            activebackground=COLOR_ROJO_CLARO,
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=8,
        ).pack(anchor="w", pady=(8, 0))
    def mostrar_citas(self):

        if not self.paciente_autenticado():
            return

        self.sistema.actualizar_citas_vencidas()
        paciente = self.paciente_actual

        citas = list(
            filter(
                lambda cita:
                    cita.paciente.codigo
                    == paciente.codigo,
                self.sistema.obtener_citas()
            )
        )

        citas = sorted(
            citas,
            key=lambda cita: cita.fecha_hora
        )

        ventana = self._crear_pantalla_interna(
            "Mis citas"
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
            width=78,
            height=17,
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

        if not citas:

            texto.insert(
                tk.END,
                "No tienes citas registradas."
            )

        else:

            for indice, cita in enumerate(
                citas,
                start=1
            ):

                texto.insert(
                    tk.END,
                    f"{indice}. "
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
                    (
                        "Especialidad: "
                        f"{cita.profesional.especialidad}\n"
                    )
                )

                texto.insert(
                    tk.END,
                    f"Estado: {cita.estado}\n"
                )

                texto.insert(
                    tk.END,
                    "\n"
                )

        texto.configure(
            state="disabled"
        )

