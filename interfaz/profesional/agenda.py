from datetime import date
import tkinter as tk
from tkinter import messagebox

from modelos.atenciones.atencion_medica import AtencionMedica
from modelos.atenciones.medicamento_recetado import MedicamentoRecetado
from servicios.gestion.sistema_salud import SistemaSalud
from servicios.validacion import validar_diagnostico
from interfaz.campos import configurar_mascara_fecha

from interfaz.estilos import (
    COLOR_FONDO,
    COLOR_PANEL,
    COLOR_PANEL_CLARO,
    COLOR_ROJO,
    COLOR_ROJO_CLARO,
    COLOR_BLANCO,
    COLOR_TEXTO,
    COLOR_GRIS_CLARO,
    COLOR_GRIS,
    FUENTE_LOGO,
    FUENTE_TITULO,
    FUENTE_SUBTITULO,
    FUENTE_SECCION,
    FUENTE_BOTON,
)
from interfaz.navegacion import (
    PASO_FINO,
    VistaDesplazable,
    comando_barra,
    desplazar_por_evento,
    instalar_navegacion,
)




class ProfesionalAgendaMixin:

    def mostrar_agenda(self):
        self._pantalla_en_edicion = False
        self._vista_actual = "agenda"
        profesional = self.profesional_actual
        self.sistema.actualizar_citas_vencidas()
        contenedor = self._marco_base(
            "Agenda profesional",
            f"{profesional.nombre} · {profesional.especialidad} · Código {profesional.codigo_profesional}",
        )
        citas = sorted(
            [
                cita
                for cita in self._citas_para_profesional()
                if not self._derivada_a_otro(cita)
                and not (
                    self._atencion_de(cita)
                    and self._atencion_de(cita).estado == "Finalizada"
                )
                and (
                    cita.estado not in {"Atendida", "No atendida", "Cancelada"}
                    or self._derivada_a_actual(cita)
                )
            ],
            key=lambda cita: cita.fecha_hora,
        )
        tk.Label(
            contenedor,
            text=f"Atenciones activas: {len(citas)}",
            font=FUENTE_SECCION,
            fg=COLOR_ROJO_CLARO,
            bg=COLOR_FONDO,
        ).pack(anchor="w", pady=(6, 12))

        accesos = tk.Frame(contenedor, bg=COLOR_FONDO)
        accesos.pack(fill="x", pady=(0, 12))
        self._boton(
            accesos, "Atenciones de hoy", self.mostrar_atenciones_hoy, COLOR_PANEL
        ).pack(side="left", padx=(0, 8))
        self._boton(
            accesos, "Historial y derivaciones", self.mostrar_historial, COLOR_PANEL
        ).pack(side="left")

        agenda = tk.Frame(contenedor, bg=COLOR_FONDO)
        agenda.pack(fill="both", expand=True)
        canvas = tk.Canvas(
            agenda,
            bg=COLOR_FONDO,
            highlightthickness=0,
            yscrollincrement=PASO_FINO,
            height=640,
        )
        barra = tk.Scrollbar(
            agenda, orient="vertical", command=comando_barra(canvas)
        )
        contenido = tk.Frame(canvas, bg=COLOR_FONDO)
        ventana_canvas = canvas.create_window(
            (0, 0), window=contenido, anchor="nw"
        )
        contenido.bind(
            "<Configure>",
            lambda evento: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.bind(
            "<Configure>",
            lambda evento: canvas.itemconfigure(ventana_canvas, width=evento.width),
        )
        canvas.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        self._enlazar_rueda(canvas, contenido)

        if not citas:
            tk.Label(
                contenido,
                text="No tienes atenciones activas asignadas.",
                font=FUENTE_SUBTITULO,
                fg=COLOR_GRIS,
                bg=COLOR_FONDO,
            ).pack(pady=24)
        for cita in citas:
            tarjeta = tk.Frame(
                contenido,
                bg=COLOR_PANEL,
                highlightbackground=COLOR_PANEL_CLARO,
                highlightthickness=1,
                padx=22,
                pady=18,
            )
            tarjeta.pack(fill="x", pady=6, padx=4)
            tk.Label(
                tarjeta,
                text=f"{cita.fecha}   ·   {cita.hora}",
                font=("Arial", 16, "bold"),
                fg=COLOR_ROJO_CLARO,
                bg=COLOR_PANEL,
            ).pack(anchor="w")
            tk.Label(
                tarjeta,
                text=(
                    f"Paciente: {cita.paciente.nombre}   ·   "
                    f"Motivo: {cita.motivo}   ·   Estado: {cita.estado}"
                ),
                font=("Arial", 12),
                fg=COLOR_TEXTO,
                bg=COLOR_PANEL,
                wraplength=900,
                justify="left",
            ).pack(anchor="w", pady=(5, 8))
            acciones = tk.Frame(tarjeta, bg=COLOR_PANEL)
            acciones.pack(anchor="w")
            if self._derivada_a_actual(cita):
                self._boton(
                    acciones,
                    "Registrar veredicto final",
                    lambda item=cita: self.editar_atencion(item),
                ).pack(side="left", padx=(0, 6))
            elif (
                cita.profesional.codigo_profesional
                == profesional.codigo_profesional
                and cita.estado in {"Pendiente", "Reprogramada", "En proceso"}
            ):
                self._boton(
                    acciones,
                    "Registrar opinión",
                    lambda item=cita: self.editar_atencion(item),
                ).pack(side="left", padx=(0, 6))
                if cita.estado in {"Pendiente", "Reprogramada"}:
                    self._boton(
                        acciones,
                        "Reprogramar",
                        lambda item=cita: self.reprogramar(item),
                        COLOR_PANEL_CLARO,
                    ).pack(side="left", padx=6)
                    self._boton(
                        acciones,
                        "Cancelar",
                        lambda item=cita: self.cancelar(item),
                        COLOR_PANEL_CLARO,
                    ).pack(side="left", padx=6)
            else:
                atencion = self._atencion_de(cita)
                if atencion:
                    self._boton(
                        acciones,
                        "Modificar opinión médica",
                        lambda item=cita: self.editar_atencion(item),
                        COLOR_PANEL_CLARO,
                    ).pack(side="left")

            atencion = self._atencion_de(cita)
            if atencion and self._derivada_a_actual(cita):
                tk.Label(
                    tarjeta,
                    text=(
                        "Informe remitente: "
                        f"{atencion.informe_derivacion or atencion.diagnostico}"
                    ),
                    font=("Arial", 10),
                    fg=COLOR_GRIS,
                    bg=COLOR_PANEL,
                    wraplength=1050,
                    justify="left",
                ).pack(anchor="w", pady=(10, 0))

        if self._temporizador:
            try:
                self.ventana.after_cancel(self._temporizador)
            except tk.TclError:
                pass
        self._temporizador = self.ventana.after(60000, self._actualizar_si_activo)
    def _citas_para_profesional(self):
        codigo = self.profesional_actual.codigo_profesional
        atenciones = {
            atencion.cita.codigo: atencion
            for atencion in self.sistema.obtener_atenciones()
        }
        return [
            cita
            for cita in self.sistema.obtener_citas()
            if cita.profesional.codigo_profesional == codigo
            or (
                atenciones.get(cita.codigo)
                and atenciones[cita.codigo].profesional_derivado
                and atenciones[cita.codigo].profesional_derivado.codigo_profesional
                == codigo
            )
        ]
    def _derivada_a_actual(self, cita):
        atencion = self._atencion_de(cita)
        return bool(
            atencion
            and atencion.profesional_derivado
            and atencion.profesional_derivado.codigo_profesional
            == self.profesional_actual.codigo_profesional
        )
    def _derivada_a_otro(self, cita):
        atencion = self._atencion_de(cita)
        return bool(
            atencion
            and atencion.profesional_derivado
            and cita.profesional.codigo_profesional
            == self.profesional_actual.codigo_profesional
            and atencion.profesional_derivado.codigo_profesional
            != self.profesional_actual.codigo_profesional
        )
    def _tarjeta_cita_profesional(self, padre, cita, permitir_edicion=False):
        atencion = self._atencion_de(cita)
        recibida = self._derivada_a_actual(cita)
        transferida = self._derivada_a_otro(cita)
        tarjeta = tk.Frame(
            padre,
            bg=COLOR_PANEL,
            highlightbackground=COLOR_PANEL_CLARO,
            highlightthickness=1,
            padx=20,
            pady=16,
        )
        tarjeta.pack(fill="x", pady=7, padx=4)
        tk.Label(
            tarjeta,
            text=f"{cita.fecha}   ·   {cita.hora}",
            font=("Arial", 15, "bold"),
            fg=COLOR_ROJO_CLARO,
            bg=COLOR_PANEL,
        ).pack(anchor="w")
        tk.Label(
            tarjeta,
            text=(
                f"Paciente: {cita.paciente.nombre}   ·   Motivo: {cita.motivo}"
            ),
            font=("Arial", 12),
            fg=COLOR_TEXTO,
            bg=COLOR_PANEL,
            wraplength=1050,
            justify="left",
        ).pack(anchor="w", pady=(6, 4))

        estado = (
            "Derivación recibida · en espera de veredicto"
            if recibida and atencion and atencion.estado != "Finalizada"
            else f"Atención: {atencion.estado}"
            if atencion
            else f"Cita: {cita.estado}"
        )
        if transferida and atencion:
            estado = f"Derivada a {atencion.profesional_derivado.nombre} · {atencion.estado}"
        tk.Label(
            tarjeta,
            text=estado,
            font=("Arial", 10, "bold"),
            fg=COLOR_ROJO if recibida or transferida else COLOR_GRIS,
            bg=COLOR_PANEL,
        ).pack(anchor="w", pady=(0, 6))

        if atencion and atencion.informe_derivacion:
            tk.Label(
                tarjeta,
                text=f"Informe remitente: {atencion.informe_derivacion}",
                font=("Arial", 10),
                fg=COLOR_GRIS,
                bg=COLOR_PANEL,
                wraplength=1050,
                justify="left",
            ).pack(anchor="w", pady=(2, 4))
        if (
            atencion
            and not transferida
            and atencion.diagnostico != atencion.informe_derivacion
        ):
            tk.Label(
                tarjeta,
                text=f"Veredicto / diagnóstico: {atencion.diagnostico}",
                font=("Arial", 11),
                fg=COLOR_TEXTO,
                bg=COLOR_PANEL,
                wraplength=1050,
                justify="left",
            ).pack(anchor="w", pady=(2, 6))

        if (
            permitir_edicion
            and not transferida
            and cita.estado in {"Pendiente", "Reprogramada", "En proceso"}
            and not (atencion and atencion.estado == "Finalizada")
        ):
            acciones = tk.Frame(tarjeta, bg=COLOR_PANEL)
            acciones.pack(anchor="w", pady=(8, 0))
            if recibida:
                self._boton(
                    acciones,
                    "Registrar veredicto final",
                    lambda item=cita: self.editar_atencion(item),
                ).pack(side="left")
            elif cita.profesional.codigo_profesional == self.profesional_actual.codigo_profesional:
                self._boton(
                    acciones,
                    "Registrar opinión",
                    lambda item=cita: self.editar_atencion(item),
                ).pack(side="left", padx=(0, 7))
                if cita.estado in {"Pendiente", "Reprogramada"}:
                    self._boton(
                        acciones,
                        "Reprogramar",
                        lambda item=cita: self.reprogramar(item),
                        COLOR_PANEL,
                    ).pack(side="left", padx=4)
                    self._boton(
                        acciones,
                        "Cancelar",
                        lambda item=cita: self.cancelar(item),
                        COLOR_PANEL,
                    ).pack(side="left", padx=4)
    def cancelar(self, cita):
        if not messagebox.askyesno(
            "Cancelar cita",
            f"¿Cancelar la cita de {cita.paciente.nombre} del {cita.fecha} a las {cita.hora}?",
        ):
            return
        try:
            self.sistema.cancelar_cita(cita.codigo)
            self.mostrar_agenda()
        except ValueError as error:
            messagebox.showerror("No se pudo cancelar", str(error))
    def reprogramar(self, cita):
        self._pantalla_en_edicion = True
        contenido = self._marco_base(
            "Reprogramar cita",
            f"Nueva fecha y horario · {cita.paciente.nombre}",
            volver=self.mostrar_agenda,
        )
        tk.Label(
            contenido,
            text=f"Nueva fecha y horario · {cita.paciente.nombre}",
            font=FUENTE_SECCION,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(padx=20, pady=(18, 10))
        tk.Label(contenido, text="Fecha (DD/MM/AAAA):", bg=COLOR_FONDO, fg=COLOR_GRIS_CLARO).pack()
        entrada_fecha = tk.Entry(contenido, width=18, justify="center")
        entrada_fecha.pack(pady=(4, 10), ipady=5)
        configurar_mascara_fecha(entrada_fecha)
        tk.Label(
            contenido,
            text="Horarios disponibles (se actualizan al salir de la fecha):",
            bg=COLOR_FONDO,
            fg=COLOR_GRIS_CLARO,
        ).pack(pady=(0, 5))
        hora_var = tk.StringVar(value="")
        opcion = tk.OptionMenu(contenido, hora_var, "")
        opcion.configure(bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO, relief="flat")
        opcion.pack(pady=(0, 12))

        def actualizar_horarios(event=None):
            try:
                horas = self.sistema.horarios_disponibles(
                    cita.profesional.codigo_profesional,
                    entrada_fecha.get(),
                    excluir_codigo=cita.codigo,
                )
            except ValueError:
                horas = []
            menu = opcion["menu"]
            menu.delete(0, "end")
            if horas:
                for hora in horas:
                    menu.add_command(
                        label=hora,
                        command=lambda valor=hora: hora_var.set(valor),
                    )
                hora_var.set(horas[0])
            else:
                menu.add_command(label="Sin horarios disponibles", command=lambda: None)
                hora_var.set("")

        entrada_fecha.bind("<FocusOut>", actualizar_horarios)
        entrada_fecha.bind("<Return>", actualizar_horarios)

        def guardar():
            try:
                if not hora_var.get():
                    raise ValueError("Selecciona un horario disponible.")
                self.sistema.reprogramar_cita(
                    cita.codigo,
                    entrada_fecha.get(),
                    hora_var.get(),
                )
                self.mostrar_agenda()
            except ValueError as error:
                messagebox.showerror("No se pudo reprogramar", str(error), parent=self.ventana)

        self._boton(contenido, "Guardar nueva fecha", guardar).pack(pady=(0, 18))

