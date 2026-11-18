import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from interfaz.campos import configurar_mascara_fecha
from modelos.especialidades import AREAS_ATENCION, ESPECIALIDADES_POR_AREA
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

        pantalla = self._crear_pantalla_interna(
            "Cita directa" if directa else "Cita regular",
            volver=self.mostrar_opciones_cita,
        )
        tk.Label(
            pantalla,
            text=f"Paciente: {self.paciente_actual.nombre}",
            font=FUENTE_SUBTITULO,
            fg=COLOR_GRIS_CLARO,
            bg=COLOR_FONDO,
        ).pack(pady=(0, 12))
        formulario = tk.Frame(pantalla, bg=COLOR_PANEL, padx=24, pady=18)
        formulario.pack(fill="x", padx=60, pady=10)
        zona = tk.Frame(formulario, bg=COLOR_PANEL)
        zona.pack(fill="x")

        def limpiar_zona():
            for widget in zona.winfo_children():
                widget.destroy()

        def volver_al_inicio_de_zona(vista):
            """Recalcula el contenido y vuelve arriba tras cambiar de vista."""
            if vista is not self.pantalla_actual or not vista.winfo_exists():
                return
            vista.update_idletasks()
            region = vista.canvas.bbox("all")
            if region is not None:
                vista.canvas.configure(scrollregion=region)
            vista.canvas.yview_moveto(0)

        def cambiar_vista():
            # Espera a que Tk procese los widgets destruidos/creados para que
            # el alto del formulario y el scrollregion reflejen la vista nueva.
            vista = self.pantalla_actual
            if vista is not None:
                self.ventana.after_idle(
                    lambda vista=vista: volver_al_inicio_de_zona(vista)
                )

        def mostrar_areas():
            limpiar_zona()
            tk.Label(
                zona,
                text="Elige el área de atención",
                font=FUENTE_BOTON,
                bg=COLOR_PANEL,
                fg=COLOR_TEXTO,
            ).pack(anchor="w", pady=(0, 8))

            panel_areas = tk.Frame(zona, bg=COLOR_PANEL)
            panel_areas.pack(fill="x")
            for indice, area in enumerate(AREAS_ATENCION):
                tk.Button(
                    panel_areas,
                    text=area,
                    command=lambda valor=area: seleccionar_area(valor),
                    font=("Arial", 9, "bold"),
                    bg=COLOR_PANEL_CLARO if indice % 2 == 0 else COLOR_BLANCO,
                    fg=COLOR_TEXTO,
                    activebackground=COLOR_ROJO_CLARO,
                    relief="flat",
                    wraplength=180,
                    width=23,
                    height=2,
                    cursor="hand2",
                ).grid(
                    row=indice // 3,
                    column=indice % 3,
                    padx=5,
                    pady=4,
                    sticky="ew",
                )
            for columna in range(3):
                panel_areas.columnconfigure(columna, weight=1)
            cambiar_vista()

        def seleccionar_area(area):
            limpiar_zona()
            tk.Button(
                zona,
                text="← Volver a áreas",
                command=mostrar_areas,
                font=FUENTE_BOTON,
                bg=COLOR_PANEL_CLARO,
                fg=COLOR_TEXTO,
                relief="flat",
                cursor="hand2",
                padx=12,
                pady=7,
            ).pack(anchor="w", pady=(0, 10))
            especialidades_area = {
                especialidad.strip().casefold()
                for especialidad in ESPECIALIDADES_POR_AREA.get(area, ())
            }
            profesionales = [
                profesional
                for profesional in self.sistema.obtener_personal()
                if "enfermer" not in profesional.especialidad.casefold()
                and profesional.especialidad.strip().casefold() in especialidades_area
            ]
            tk.Label(
                zona,
                text=f"Profesionales del área de {area}",
                font=FUENTE_BOTON,
                bg=COLOR_PANEL,
                fg=COLOR_TEXTO,
            ).pack(anchor="w", pady=(10, 6))
            if not profesionales:
                tk.Label(
                    zona,
                    text="Esta área todavía no tiene profesionales registrados. Elige otra área.",
                    bg=COLOR_PANEL,
                    fg=COLOR_ROJO,
                    wraplength=700,
                    justify="left",
                ).pack(anchor="w", pady=(0, 10))
                cambiar_vista()
                return
            tk.Label(
                zona,
                text="Selecciona al profesional que deseas atenderte:",
                bg=COLOR_PANEL,
                fg=COLOR_TEXTO,
            ).pack(anchor="w", pady=(0, 8))
            panel_profesionales = tk.Frame(zona, bg=COLOR_PANEL)
            panel_profesionales.pack(fill="x", pady=(0, 10))
            for indice, profesional in enumerate(profesionales):
                tarjeta = tk.Button(
                    panel_profesionales,
                    text=(
                        f"{profesional.nombre}\n"
                        f"Edad: {profesional.edad} años\n"
                        f"Código profesional: {profesional.codigo_profesional}\n"
                        "Seleccionar profesional"
                    ),
                    command=lambda item=profesional: mostrar_reserva(item, area),
                    font=("Arial", 10, "bold"),
                    bg=COLOR_PANEL_CLARO,
                    fg=COLOR_TEXTO,
                    activebackground=COLOR_ROJO_CLARO,
                    activeforeground=COLOR_BLANCO,
                    relief="flat",
                    anchor="w",
                    justify="left",
                    wraplength=240,
                    width=31,
                    height=5,
                    cursor="hand2",
                    padx=12,
                    pady=10,
                )
                tarjeta.grid(
                    row=indice // 3,
                    column=indice % 3,
                    padx=5,
                    pady=5,
                    sticky="ew",
                )
            for columna in range(3):
                panel_profesionales.columnconfigure(columna, weight=1)
            cambiar_vista()

        def mostrar_reserva(profesional=None, area=None):
            limpiar_zona()
            if profesional is None and directa:
                return
            if directa:
                tk.Button(
                    zona,
                    text="← Volver a profesionales",
                    command=lambda: seleccionar_area(area),
                    font=FUENTE_BOTON,
                    bg=COLOR_PANEL_CLARO,
                    fg=COLOR_TEXTO,
                    relief="flat",
                    cursor="hand2",
                    padx=12,
                    pady=7,
                ).pack(anchor="w", pady=(0, 10))
            tk.Label(
                zona,
                text=(
                    f"Profesional elegido: {profesional.nombre} · {profesional.especialidad}"
                    if profesional
                    else "Cita regular con el personal de triaje"
                ),
                font=FUENTE_BOTON,
                bg=COLOR_PANEL,
                fg=COLOR_TEXTO,
            ).pack(anchor="w", pady=(5, 12))
            selecciones_sintomas, entrada_otro = self._crear_selector_sintomas(zona)
            tk.Label(
                zona,
                text="Fecha (DD/MM/AAAA):",
                bg=COLOR_PANEL,
                fg=COLOR_TEXTO,
            ).pack(anchor="w")
            entrada_fecha = tk.Entry(
                zona,
                width=20,
                justify="center",
                bg=COLOR_PANEL_CLARO,
                fg=COLOR_TEXTO,
                insertbackground=COLOR_TEXTO,
                relief="flat",
            )
            entrada_fecha.pack(anchor="w", pady=(4, 12), ipady=6)
            configurar_mascara_fecha(entrada_fecha)
            entrada_fecha.delete(0, tk.END)
            tk.Label(
                zona,
                text="Horarios disponibles · turnos de 20 minutos (07:00–17:40):",
                font=FUENTE_BOTON,
                bg=COLOR_PANEL,
                fg=COLOR_TEXTO,
            ).pack(anchor="w")
            hora_var = tk.StringVar(value="")
            menu_hora = tk.OptionMenu(zona, hora_var, "")
            menu_hora.configure(bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO, relief="flat")
            menu_hora.pack(anchor="w", pady=(4, 10))

            def actualizar_horarios(event=None):
                try:
                    fecha = normalizar_fecha(entrada_fecha.get())
                    if directa:
                        horarios = self.sistema.horarios_disponibles_para_profesional(
                            profesional.codigo_profesional,
                            fecha,
                            paciente_codigo=self.paciente_actual.codigo,
                        )
                    else:
                        horarios = self.sistema.horarios_disponibles_para_triaje(
                            fecha,
                            paciente_codigo=self.paciente_actual.codigo,
                        )
                except ValueError:
                    horarios = []
                menu = menu_hora["menu"]
                menu.delete(0, "end")
                if horarios:
                    for disponible in horarios:
                        menu.add_command(
                            label=disponible,
                            command=lambda valor=disponible: hora_var.set(valor),
                        )
                    hora_var.set(horarios[0])
                else:
                    menu.add_command(
                        label="Sin horarios para esa fecha",
                        command=lambda: None,
                    )
                    hora_var.set("")

            tk.Button(
                zona,
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
            ).pack(anchor="w", pady=(0, 12))
            entrada_fecha.bind("<FocusOut>", actualizar_horarios)
            entrada_fecha.bind("<Return>", actualizar_horarios)

            def guardar():
                try:
                    fecha = normalizar_fecha(entrada_fecha.get())
                    if not hora_var.get():
                        raise ValueError("Selecciona un horario disponible.")
                    motivo = self._obtener_motivo_sintomas(
                        selecciones_sintomas,
                        entrada_otro,
                    )
                    if directa:
                        cita = self.sistema.crear_cita_directa(
                            self.paciente_actual,
                            profesional,
                            fecha,
                            motivo,
                            hora_var.get(),
                        )
                    else:
                        cita = self.sistema.crear_cita_regular(
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
                except (TypeError, ValueError) as error:
                    messagebox.showerror("No se pudo registrar la cita", str(error))

            tk.Button(
                zona,
                text="Confirmar cita",
                command=guardar,
                font=FUENTE_BOTON,
                bg=COLOR_ROJO,
                fg=COLOR_BLANCO,
                activebackground=COLOR_ROJO_CLARO,
                relief="flat",
                cursor="hand2",
                padx=16,
                pady=9,
            ).pack(anchor="w", pady=(8, 0))
            if directa:
                cambiar_vista()

        if directa:
            mostrar_areas()
        else:
            tk.Label(
                formulario,
                text=(
                    "La cita regular inicia en triaje. El personal registrará la valoración; "
                    "después el sistema asignará una consulta con medicina general."
                ),
                bg=COLOR_PANEL,
                fg=COLOR_TEXTO,
                wraplength=760,
                justify="left",
            ).pack(anchor="w", pady=(0, 10))
            if not self.sistema.obtener_personal_triaje():
                tk.Label(
                    formulario,
                    text="No hay técnicos de triaje con cuenta activa para asignar citas.",
                    bg=COLOR_PANEL,
                    fg=COLOR_ROJO,
                ).pack(anchor="w")
            else:
                mostrar_reserva()

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
                    f"Tipo: {cita.tipo_cita}\n"
                )
                valoracion = self.sistema.obtener_valoracion_para_cita(cita)
                if valoracion:
                    texto.insert(
                        tk.END,
                        f"Triaje: nivel {valoracion.nivel} · {valoracion.color}\n"
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
