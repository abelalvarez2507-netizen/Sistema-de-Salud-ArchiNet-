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




class ProfesionalAtencionesMixin:

    def mostrar_atenciones_hoy(self):
        self._pantalla_en_edicion = False
        self._vista_actual = "hoy"
        self.sistema.actualizar_citas_vencidas()
        hoy = date.today().strftime("%d/%m/%Y")
        contenido = self._marco_base(
            "Atenciones de hoy",
            f"Agenda y atenciones del {hoy} · {self.profesional_actual.nombre}",
            volver=self.mostrar_agenda,
        )
        citas = sorted(
            [
                cita for cita in self._citas_para_profesional()
                if cita.fecha == hoy and not self._derivada_a_otro(cita)
            ],
            key=lambda cita: cita.fecha_hora,
        )
        if not citas:
            tk.Label(
                contenido,
                text="No tienes atenciones registradas para hoy.",
                font=FUENTE_SUBTITULO,
                fg=COLOR_GRIS,
                bg=COLOR_FONDO,
            ).pack(anchor="w", pady=20)
        for cita in citas:
            self._tarjeta_cita_profesional(contenido, cita, permitir_edicion=True)
    def _atencion_de(self, cita):
        return next(
            (
                atencion
                for atencion in self.sistema.obtener_atenciones()
                if atencion.cita.codigo == cita.codigo
            ),
            None,
        )
    def editar_atencion(self, cita):
        atencion = self._atencion_de(cita)
        self._pantalla_en_edicion = True
        contenido = self._marco_base(
            "Opinión médica",
            f"Atención a {cita.paciente.nombre} · {cita.fecha} {cita.hora}",
            volver=self.mostrar_agenda,
        )
        tk.Label(
            contenido,
            text=f"Atención a {cita.paciente.nombre} · {cita.fecha} {cita.hora}",
            font=FUENTE_SECCION,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(padx=22, pady=(18, 10))
        if atencion and self._derivada_a_actual(cita):
            marco_informe = tk.Frame(contenido, bg=COLOR_PANEL, padx=14, pady=12)
            marco_informe.pack(fill="x", padx=22, pady=(0, 10))
            tk.Label(
                marco_informe,
                text="Informe del profesional remitente",
                font=("Arial", 16, "bold"),
                fg=COLOR_TEXTO,
                bg=COLOR_PANEL,
            ).pack(anchor="w")
            tk.Label(
                marco_informe,
                text=atencion.informe_derivacion or atencion.diagnostico,
                font=("Arial", 12),
                fg=COLOR_TEXTO,
                bg=COLOR_PANEL,
                wraplength=1000,
                justify="left",
            ).pack(anchor="w", pady=(4, 0))
        tk.Label(
            contenido,
            text="Opinión médica / diagnóstico:",
            font=FUENTE_BOTON,
            fg=COLOR_GRIS_CLARO,
            bg=COLOR_FONDO,
        ).pack(anchor="w", padx=22)
        texto = tk.Text(
            contenido,
            width=62,
            height=7,
            wrap="word",
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="flat",
        )
        texto.pack(fill="x", padx=22, pady=8)
        if atencion and not self._derivada_a_actual(cita):
            texto.insert("1.0", atencion.diagnostico)

        es_medico_general = (
            self.profesional_actual.especialidad.strip().casefold()
            == "medicina general"
        )
        opciones_derivacion = {}
        derivacion_var = None
        if es_medico_general:
            panel_derivacion = tk.Frame(contenido, bg=COLOR_PANEL, padx=14, pady=12)
            panel_derivacion.pack(fill="x", padx=22, pady=(4, 10))
            tk.Label(
                panel_derivacion,
                text="Derivar a",
                font=("Arial", 16, "bold"),
                fg=COLOR_TEXTO,
                bg=COLOR_PANEL,
            ).pack(anchor="w")
            especialistas = [
                profesional
                for profesional in self.sistema.obtener_personal()
                if profesional.codigo_profesional
                != self.profesional_actual.codigo_profesional
                and "enfermer" not in profesional.especialidad.casefold()
                and profesional.especialidad.strip().casefold()
                != "medicina general"
            ]
            etiqueta_vacia = "-- Selecciona el profesional derivado --"
            opciones_derivacion[etiqueta_vacia] = None
            for profesional in especialistas:
                etiqueta = (
                    f"{profesional.codigo_profesional} · {profesional.nombre} · "
                    f"{profesional.especialidad}"
                )
                opciones_derivacion[etiqueta] = profesional

            if atencion and atencion.profesional_derivado:
                profesional_guardado = atencion.profesional_derivado
                etiqueta_guardada = (
                    f"{profesional_guardado.codigo_profesional} · "
                    f"{profesional_guardado.nombre} · "
                    f"{profesional_guardado.especialidad}"
                )
                opciones_derivacion[etiqueta_guardada] = profesional_guardado
                valor_inicial = etiqueta_guardada
            else:
                valor_inicial = etiqueta_vacia

            derivacion_var = tk.StringVar(value=valor_inicial)
            menu_derivacion = tk.OptionMenu(
                panel_derivacion,
                derivacion_var,
                *opciones_derivacion,
            )
            menu_derivacion.configure(
                bg=COLOR_PANEL_CLARO,
                fg=COLOR_TEXTO,
                relief="flat",
            )
            menu_derivacion.pack(anchor="w")
            if not especialistas:
                tk.Label(
                    panel_derivacion,
                    text="No hay profesionales disponibles para derivación.",
                    font=("Arial", 9),
                    fg=COLOR_ROJO,
                    bg=COLOR_PANEL,
                ).pack(anchor="w", pady=(5, 0))

        panel_recetas = tk.Frame(contenido, bg=COLOR_PANEL, padx=14, pady=12)
        panel_recetas.pack(fill="x", padx=22, pady=(4, 10))
        tk.Label(
            panel_recetas,
            text="Medicamentos recetados",
            font=FUENTE_SECCION,
            fg=COLOR_TEXTO,
            bg=COLOR_PANEL,
        ).pack(anchor="w")
        encabezados = tk.Frame(panel_recetas, bg=COLOR_PANEL)
        encabezados.pack(fill="x")
        for columna, (titulo, peso) in enumerate((("Medicamento", 3), ("Días", 1), ("Cada cuánto", 2))):
            encabezados.columnconfigure(columna, weight=peso)
            tk.Label(
                encabezados,
                text=titulo,
                font=FUENTE_BOTON,
                fg=COLOR_GRIS_CLARO,
                bg=COLOR_PANEL,
            ).grid(row=0, column=columna, sticky="w", padx=3)

        filas_recetas = []
        contenedor_filas = tk.Frame(panel_recetas, bg=COLOR_PANEL)
        contenedor_filas.pack(fill="x")

        def agregar_fila_receta(medicamento="", dias="", cada_cuanto=""):
            fila = tk.Frame(contenedor_filas, bg=COLOR_PANEL)
            fila.pack(fill="x", pady=3)
            campos = []
            for columna, (valor, peso) in enumerate(((medicamento, 3), (dias, 1), (cada_cuanto, 2))):
                entrada = tk.Entry(
                    fila,
                    font=FUENTE_BOTON,
                    bg=COLOR_PANEL_CLARO,
                    fg=COLOR_TEXTO,
                    insertbackground=COLOR_TEXTO,
                    relief="flat",
                )
                entrada.grid(row=0, column=columna, sticky="ew", padx=3, ipady=6)
                fila.columnconfigure(columna, weight=peso)
                if valor:
                    entrada.insert(0, str(valor))
                campos.append(entrada)
            def quitar():
                fila.destroy()
                filas_recetas.remove(campos)
            tk.Button(
                fila,
                text="Quitar",
                command=quitar,
                font=FUENTE_BOTON,
                bg=COLOR_PANEL_CLARO,
                fg=COLOR_TEXTO,
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=8,
            ).grid(row=0, column=3, padx=(4, 0))
            filas_recetas.append(campos)

        if atencion and atencion.recetas:
            for receta in atencion.recetas:
                agregar_fila_receta(receta.medicamento, receta.dias, receta.cada_cuanto)
        else:
            agregar_fila_receta()

        self._boton(
            panel_recetas,
            "+ Agregar medicamento",
            agregar_fila_receta,
            COLOR_PANEL_CLARO,
        ).pack(anchor="w", pady=(8, 0))

        def leer_recetas():
            recetas = []
            for medicamento, dias, cada_cuanto in filas_recetas:
                valores = (medicamento.get().strip(), dias.get().strip(), cada_cuanto.get().strip())
                if not any(valores):
                    continue
                recetas.append(MedicamentoRecetado(*valores))
            return recetas

        def guardar():
            try:
                diagnostico = validar_diagnostico(texto.get("1.0", "end-1c"))
                recetas = leer_recetas()
                profesional_derivado = None
                if es_medico_general:
                    profesional_derivado = opciones_derivacion.get(
                        derivacion_var.get()
                    )
                    if profesional_derivado is None:
                        raise ValueError(
                            "Selecciona al especialista al que se derivará al paciente."
                        )
                if atencion:
                    self.sistema.actualizar_atencion(
                        atencion.codigo,
                        diagnostico,
                        recetas,
                        profesional_derivado,
                        profesional_autor=self.profesional_actual,
                    )
                else:
                    atencion_nueva = AtencionMedica(
                        self.sistema.generar_codigo_atencion(),
                        cita,
                        diagnostico,
                        "En proceso" if profesional_derivado else "Finalizada",
                        recetas,
                        profesional_derivado,
                    )
                    self.sistema.registrar_atencion(atencion_nueva)
                messagebox.showinfo(
                    "Atención guardada",
                    (
                        "El informe y la derivación se guardaron. La atención sigue "
                        "en proceso en la agenda del profesional derivado."
                        if profesional_derivado
                        else "La opinión médica y las recetas se guardaron; "
                        "la cita quedó marcada como atendida."
                    ),
                    parent=self.ventana,
                )
                self.mostrar_agenda()
            except (TypeError, ValueError) as error:
                messagebox.showerror("No se pudo guardar", str(error), parent=self.ventana)

        self._boton(contenido, "Guardar opinión y receta", guardar).pack(pady=(0, 18))
    def marcar_no_atendida(self, cita):
        if not messagebox.askyesno(
            "Confirmar estado",
            f"¿Marcar como no atendida la cita de {cita.paciente.nombre}?",
        ):
            return
        try:
            self.sistema.actualizar_estado_cita(cita.codigo, "No atendida")
            self.mostrar_agenda()
        except ValueError as error:
            messagebox.showerror("No se pudo actualizar", str(error))

