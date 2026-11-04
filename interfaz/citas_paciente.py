import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from interfaz.campos import configurar_mascara_fecha
from interfaz.estilos import (
    COLOR_BLANCO,
    COLOR_FONDO,
    COLOR_GRIS,
    COLOR_GRIS_CLARO,
    COLOR_PANEL,
    COLOR_PANEL_CLARO,
    COLOR_ROJO,
    COLOR_ROJO_CLARO,
    COLOR_TEXTO,
    FUENTE_BOTON,
    FUENTE_SUBTITULO,
)
from servicios.validaciones import normalizar_fecha


SINTOMAS_CITA = (
    "Tos seca",
    "Tos con flema",
    "Fiebre",
    "Escalofríos",
    "Congestión nasal",
    "Dolor de garganta",
    "Dolor de cabeza",
    "Mareos",
    "Dificultad para respirar",
    "Dolor de pecho",
    "Dolor abdominal",
    "Náuseas",
    "Vómitos",
    "Diarrea",
    "Fatiga",
    "Dolor muscular",
    "Dolor articular",
    "Erupción en la piel",
    "Ardor al orinar",
    "Dolor de oído",
)


class PacienteCitasMixin:
    # Comparte las operaciones de citas entre las dos modalidades.

    # =========================================================
    # SOLICITAR CITA
    # =========================================================

    def mostrar_opciones_cita(self):
        if not self.paciente_autenticado():
            return

        pantalla = self._crear_pantalla_interna("Citas")
        tk.Label(
            pantalla,
            text=f"Paciente: {self.paciente_actual.nombre}",
            font=FUENTE_SUBTITULO,
            fg=COLOR_GRIS_CLARO,
            bg=COLOR_FONDO,
        ).pack(pady=(0, 12))

        opciones = tk.Frame(pantalla, bg=COLOR_FONDO)
        opciones.pack(pady=8)

        tarjeta_directa = self.crear_tarjeta(
            opciones,
            "Cita directa",
            "",
            self.solicitar_cita_directa,
        )
        tarjeta_directa.grid(row=0, column=0, padx=15, pady=10)

        tarjeta_regular = self.crear_tarjeta(
            opciones,
            "Cita regular",
            "",
            self.solicitar_cita,
        )
        tarjeta_regular.grid(row=0, column=1, padx=15, pady=10)

    def _crear_selector_sintomas(self, formulario):
        tk.Label(
            formulario,
            text="Motivo de la cita:",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        ).pack(anchor="w")

        panel_sintomas = tk.Frame(formulario, bg=COLOR_PANEL)
        panel_sintomas.pack(fill="x", pady=(4, 8))

        selecciones = []
        columnas = 3
        for indice, sintoma in enumerate(SINTOMAS_CITA):
            seleccionado = tk.IntVar(master=panel_sintomas, value=0)
            casilla = tk.Checkbutton(
                panel_sintomas,
                text=sintoma,
                variable=seleccionado,
                onvalue=1,
                offvalue=0,
                font=("Arial", 10),
                bg=COLOR_PANEL,
                fg=COLOR_TEXTO,
                activebackground=COLOR_PANEL,
                selectcolor=COLOR_PANEL_CLARO,
                anchor="w",
                wraplength=175,
            )
            casilla.grid(
                row=indice // columnas,
                column=indice % columnas,
                sticky="w",
                padx=(0, 12),
                pady=2,
            )
            selecciones.append((sintoma, seleccionado))

        tk.Label(
            formulario,
            text="Otro síntoma:",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        ).pack(anchor="w")
        entrada_otro = tk.Entry(
            formulario,
            width=55,
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="flat",
        )
        entrada_otro.pack(anchor="w", pady=(4, 8), ipady=6)

        return selecciones, entrada_otro

    @staticmethod
    def _obtener_motivo_sintomas(selecciones, entrada_otro):
        sintomas = [
            sintoma
            for sintoma, seleccionado in selecciones
            if seleccionado.get()
        ]
        otro_sintoma = entrada_otro.get().strip()
        if otro_sintoma:
            sintomas.append(otro_sintoma)
        if not sintomas:
            raise ValueError("Selecciona o escribe al menos un síntoma.")
        return ", ".join(sintomas)

    def solicitar_cita_directa(self):
        self._mostrar_formulario_cita(directa=True)

    def solicitar_cita(self):
        self._mostrar_formulario_cita(directa=False)

    def _mostrar_formulario_cita(self, directa):
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

        pantalla = self._crear_pantalla_interna(
            "Cita directa" if directa else "Cita regular",
            volver=self.mostrar_opciones_cita,
        )
        encabezado_cita = tk.Frame(pantalla, bg=COLOR_FONDO)
        encabezado_cita.pack(fill="x", padx=60, pady=(0, 12))
        tk.Label(
            encabezado_cita,
            text=f"Paciente: {self.paciente_actual.nombre}",
            font=FUENTE_SUBTITULO,
            fg=COLOR_GRIS_CLARO,
            bg=COLOR_FONDO,
        ).pack()

        etiqueta_generacion = tk.Label(
            encabezado_cita,
            text="",
            font=("Arial", 9, "bold"),
            fg=COLOR_ROJO,
            bg=COLOR_FONDO,
            anchor="e",
        )
        etiqueta_generacion.place(relx=1, rely=0.5, anchor="e")

        def actualizar_reloj_generacion():
            try:
                ahora = datetime.now()
                etiqueta_generacion.configure(
                    text=(
                        "Fecha y hora de generación de cita: "
                        f"{ahora.strftime('%d/%m/%Y %H:%M:%S')}"
                    )
                )
                etiqueta_generacion.after(1000, actualizar_reloj_generacion)
            except tk.TclError:
                return

        actualizar_reloj_generacion()

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
        # Ambas modalidades comienzan sin una fecha seleccionada.
        entrada_fecha.delete(0, tk.END)

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

        selecciones_sintomas, entrada_otro = self._crear_selector_sintomas(formulario)

        def guardar():
            try:
                fecha = normalizar_fecha(entrada_fecha.get())
                if not hora_var.get():
                    raise ValueError("Selecciona un horario disponible.")
                motivo = self._obtener_motivo_sintomas(
                    selecciones_sintomas,
                    entrada_otro,
                )
                cita = self.sistema.crear_cita_asignacion_automatica(
                    self.paciente_actual,
                    fecha,
                    motivo,
                    hora_var.get(),
                )
                messagebox.showinfo(
                    "Cita solicitada",
                    (
                        "Tu cita se generó el "
                        f"{cita.fecha_generacion.strftime('%d/%m/%Y %H:%M:%S')} "
                        f"y quedó agendada para el {cita.fecha} a las {cita.hora}.\n"
                        f"Profesional: {cita.profesional.nombre} "
                        f"({cita.profesional.especialidad})."
                    ),
                )
                self.crear_interfaz()
            except ValueError as error:
                messagebox.showerror("No se pudo registrar la cita", str(error))

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

    # =========================================================
    # MIS CITAS
    # =========================================================

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
                    "Generada: "
                    + (
                        cita.fecha_generacion.strftime("%d/%m/%Y %H:%M:%S")
                        if cita.fecha_generacion
                        else "No registrada"
                    )
                    + "\n",
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
