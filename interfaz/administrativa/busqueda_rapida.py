
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


from interfaz.administrativa.pacientes.menus import PacientesMenusMixin
from interfaz.administrativa.pacientes.registro import PacientesRegistroMixin
from interfaz.administrativa.pacientes.consulta import PacientesConsultaMixin
from interfaz.administrativa.pacientes.historial import PacientesHistorialMixin



class AdministrativoBusquedaMixin:

    def _crear_busqueda_rapida(self, interior):
        # Construye el formulario y sus manejadores de búsqueda.
        tarjeta_busqueda = tk.Frame(
            interior,
            bg=COLOR_PANEL,
            highlightbackground=COLOR_PANEL_CLARO,
            highlightthickness=1,
        )

        tarjeta_busqueda.pack(
            fill="x",
            pady=(0, 15),
        )

        cabecera_busqueda = tk.Frame(
            tarjeta_busqueda,
            bg=COLOR_PANEL,
        )

        cabecera_busqueda.pack(
            fill="x",
            padx=14,
            pady=(10, 2),
        )

        tk.Label(
            cabecera_busqueda,
            text="🔎",
            font=("Arial", 16, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_ROJO,
        ).pack(side="left")

        instrucciones_busqueda = tk.Frame(
            cabecera_busqueda,
            bg=COLOR_PANEL,
        )

        instrucciones_busqueda.pack(
            side="left",
            padx=(9, 0),
        )

        tk.Label(
            instrucciones_busqueda,
            text="BÚSQUEDA RÁPIDA",
            font=FUENTE_NORMAL_BOLD,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        ).pack(anchor="w")

        tk.Label(
            instrucciones_busqueda,
            text="Código o DNI.",
            font=FUENTE_PEQUENA,
            bg=COLOR_PANEL,
            fg=COLOR_GRIS,
        ).pack(anchor="w")

        fila_busqueda_rapida = tk.Frame(
            tarjeta_busqueda,
            bg=COLOR_PANEL,
        )

        fila_busqueda_rapida.pack(
            fill="x",
            padx=14,
            pady=(6, 12),
        )

        fila_busqueda_rapida.columnconfigure(0, weight=1)

        valor_busqueda_rapida = tk.StringVar(
            master=self.ventana,
        )

        entrada_busqueda_rapida = tk.Entry(
            fila_busqueda_rapida,
            textvariable=valor_busqueda_rapida,
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="flat",
            bd=0,
            font=FUENTE_NORMAL,
        )

        entrada_busqueda_rapida.grid(
            row=0,
            column=0,
            sticky="ew",
            ipady=9,
            padx=(0, 10),
        )

        self.configurar_limite_busqueda(
            entrada_busqueda_rapida,
            self.ventana,
            maximo=None,
        )

        mensaje_busqueda = tk.Label(
            interior,
            text="",
            font=FUENTE_PEQUENA,
            bg=COLOR_FONDO,
            fg=COLOR_ERROR,
            anchor="w",
        )

        def mostrar_mensaje_busqueda(mensaje):
            mensaje_busqueda.configure(text=mensaje)
            if not mensaje_busqueda.winfo_manager():
                mensaje_busqueda.pack(
                    fill="x",
                    padx=14,
                    pady=(0, 12),
                    after=tarjeta_busqueda,
                )

        def limpiar_mensaje_busqueda(*_args):
            mensaje_busqueda.configure(text="")
            if mensaje_busqueda.winfo_manager():
                mensaje_busqueda.pack_forget()

        def presentar_resultado_busqueda(contenido):
            pantalla_resultado = self._crear_pantalla_interna(
                "Resultado de búsqueda rápida"
            )

            tk.Label(
                pantalla_resultado,
                text="RESULTADO DE BÚSQUEDA",
                font=FUENTE_TITULO,
                bg=COLOR_FONDO,
                fg=COLOR_TEXTO,
            ).pack(
                anchor="w",
                padx=24,
                pady=(20, 10),
            )

            marco_resultado = tk.Frame(
                pantalla_resultado,
                bg=COLOR_PANEL,
                highlightbackground=COLOR_PANEL_CLARO,
                highlightthickness=1,
            )

            marco_resultado.pack(
                fill="both",
                expand=True,
                padx=24,
                pady=(0, 24),
            )

            texto_resultado = tk.Text(
                marco_resultado,
                height=24,
                wrap="word",
                bg=COLOR_PANEL,
                fg=COLOR_TEXTO,
                insertbackground=COLOR_TEXTO,
                relief="flat",
                bd=0,
                padx=14,
                pady=12,
                font=FUENTE_NORMAL,
            )

            barra_resultado = tk.Scrollbar(
                marco_resultado,
                orient="vertical",
                command=texto_resultado.yview,
            )

            texto_resultado.configure(
                yscrollcommand=barra_resultado.set,
            )
            texto_resultado.pack(
                side="left",
                fill="both",
                expand=True,
            )
            barra_resultado.pack(
                side="right",
                fill="y",
            )
            texto_resultado.insert(tk.END, contenido)
            texto_resultado.configure(state="disabled")
            texto_resultado.see("1.0")

        def buscar_rapido(evento=None):
            valor = entrada_busqueda_rapida.get().strip()

            if len(valor) < 2:
                return "break"

            if not self.validar_entrada_busqueda(valor):
                mostrar_mensaje_busqueda(
                    "Usa únicamente letras, números, guion o guion bajo."
                )
                return "break"

            limpiar_mensaje_busqueda()

            try:
                pacientes_encontrados = (
                    self.sistema.buscar_paciente_por_codigo(valor)
                )
                profesionales_encontrados = (
                    self.sistema.buscar_personal_por_codigo(valor)
                )

                if valor.isdigit() and len(valor) == 8:
                    dni = self.validar_dni(valor)
                    pacientes_por_dni = self.sistema.buscar_paciente_por_dni(dni)
                    profesionales_por_dni = (
                        self.sistema.buscar_personal_por_dni(dni)
                    )
                    pacientes_encontrados.extend(
                        paciente
                        for paciente in pacientes_por_dni
                        if all(
                            existente.codigo != paciente.codigo
                            for existente in pacientes_encontrados
                        )
                    )
                    profesionales_encontrados.extend(
                        profesional
                        for profesional in profesionales_por_dni
                        if all(
                            existente.codigo_profesional
                            != profesional.codigo_profesional
                            for existente in profesionales_encontrados
                        )
                    )
            except (ValueError, TypeError) as error:
                mostrar_mensaje_busqueda(str(error))
                return "break"

            citas = self.sistema.obtener_citas()
            atenciones = self.sistema.obtener_atenciones()
            atenciones_por_cita = {
                atencion.cita.codigo: atencion
                for atencion in atenciones
            }
            bloques = []

            for paciente in pacientes_encontrados:
                citas_paciente = sorted(
                    (
                        cita
                        for cita in citas
                        if cita.paciente.codigo == paciente.codigo
                    ),
                    key=lambda cita: cita.fecha_hora,
                    reverse=True,
                )
                ventas_paciente = self.sistema.obtener_historial_paciente(
                    paciente.codigo
                ).get("ventas_medicamentos", [])

                bloques.extend((
                    "FICHA DEL PACIENTE",
                    f"Código: {paciente.codigo}",
                    f"DNI: {paciente.dni_mascarado}",
                    f"Nombre: {paciente.nombre}",
                    f"Edad: {paciente.edad} años",
                    "",
                    "CITAS Y ATENCIONES",
                ))

                if not citas_paciente:
                    bloques.append("No tiene citas registradas.")

                for cita in citas_paciente:
                    bloques.extend((
                        "",
                        f"Cita {cita.codigo} · {cita.fecha} {cita.hora}",
                        f"Motivo: {cita.motivo}",
                        f"Estado de la cita: {cita.estado}",
                        (
                            f"Profesional asignado: {cita.profesional.nombre} "
                            f"({cita.profesional.codigo_profesional})"
                        ),
                        f"Especialidad: {cita.profesional.especialidad}",
                    ))

                    atencion = atenciones_por_cita.get(cita.codigo)
                    if atencion is None:
                        bloques.append("Atención: todavía no registrada.")
                    else:
                        bloques.extend((
                            f"Código de atención: {atencion.codigo}",
                            (
                                f"Atendido por: {atencion.profesional.nombre} "
                                f"({atencion.profesional.codigo_profesional})"
                            ),
                            f"Diagnóstico: {atencion.diagnostico}",
                            f"Estado de la atención: {atencion.estado}",
                        ))
                        if atencion.informe_derivacion and atencion.informe_derivacion != atencion.diagnostico:
                            bloques.append(
                                f"Informe de derivación: {atencion.informe_derivacion}"
                            )
                        if atencion.profesional_derivado:
                            bloques.append(
                                f"Derivado a: {atencion.profesional_derivado.nombre} "
                                f"({atencion.profesional_derivado.especialidad})"
                            )
                        if atencion.recetas:
                            bloques.append("Medicamentos recetados:")
                            bloques.extend(
                                f"  • {receta.mostrar_informacion()}"
                                for receta in atencion.recetas
                            )

                bloques.append("MEDICAMENTOS REGISTRADOS EN VENTA")
                if not ventas_paciente:
                    bloques.append("No hay ventas de medicamentos vinculadas.")
                else:
                    for venta in ventas_paciente:
                        (_id, medicamento, lote, cantidad, _precio, total, codigo, vendedor, fecha_hora) = venta
                        bloques.append(
                            f"{fecha_hora} · {medicamento} · Lote {lote} · "
                            f"{cantidad} unidad(es) · S/ {float(total):.2f} · Paciente {codigo}"
                        )

                bloques.extend((
                    "",
                    f"Resumen: {len(citas_paciente)} cita(s), "
                    f"{sum(cita.codigo in atenciones_por_cita for cita in citas_paciente)} "
                    "atención(es).",
                    "",
                ))

            for profesional in profesionales_encontrados:
                citas_profesional = sorted(
                    (
                        cita
                        for cita in citas
                        if (
                            cita.profesional.codigo_profesional
                            == profesional.codigo_profesional
                        )
                    ),
                    key=lambda cita: cita.fecha_hora,
                    reverse=True,
                )

                bloques.extend((
                    "FICHA DEL PROFESIONAL",
                    f"Código profesional: {profesional.codigo_profesional}",
                    f"DNI: {profesional.dni_mascarado}",
                    f"Nombre: {profesional.nombre}",
                    f"Edad: {profesional.edad} años",
                    f"Especialidad: {profesional.especialidad}",
                    "",
                    "PACIENTES, CITAS Y ATENCIONES",
                ))

                if not citas_profesional:
                    bloques.append("No tiene citas registradas.")

                for cita in citas_profesional:
                    bloques.extend((
                        "",
                        f"Paciente: {cita.paciente.nombre}",
                        f"Código de paciente: {cita.paciente.codigo}",
                        f"DNI: {cita.paciente.dni_mascarado}",
                        f"Edad: {cita.paciente.edad} años",
                        f"Cita {cita.codigo} · {cita.fecha} {cita.hora}",
                        f"Motivo: {cita.motivo}",
                        f"Estado de la cita: {cita.estado}",
                    ))

                    atencion = atenciones_por_cita.get(cita.codigo)
                    if atencion is None:
                        bloques.append("Atención: todavía no registrada.")
                    else:
                        bloques.extend((
                            (
                                f"Atendido por: {atencion.profesional.nombre} "
                                f"({atencion.profesional.codigo_profesional})"
                            ),
                            f"Diagnóstico: {atencion.diagnostico}",
                            f"Estado de la atención: {atencion.estado}",
                        ))
                        if atencion.informe_derivacion and atencion.informe_derivacion != atencion.diagnostico:
                            bloques.append(
                                f"Informe de derivación: {atencion.informe_derivacion}"
                            )
                        if atencion.profesional_derivado:
                            bloques.append(
                                f"Derivado a: {atencion.profesional_derivado.nombre} "
                                f"({atencion.profesional_derivado.especialidad})"
                            )

                bloques.extend((
                    "",
                    f"Resumen: {len(citas_profesional)} cita(s), "
                    f"{sum(cita.codigo in atenciones_por_cita for cita in citas_profesional)} "
                    "atención(es).",
                    "",
                ))

            if not bloques:
                mostrar_mensaje_busqueda(
                    "No se encontró un paciente ni profesional con ese "
                    "código o DNI."
                )
            else:
                presentar_resultado_busqueda("\n".join(bloques).strip())

            return "break"

        boton_buscar_rapido = tk.Button(
            fila_busqueda_rapida,
            text="Buscar",
            command=buscar_rapido,
            font=FUENTE_BOTON,
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_GRIS,
            disabledforeground=COLOR_GRIS,
            state=tk.DISABLED,
            activebackground=COLOR_ROJO_CLARO,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=22,
            pady=8,
        )

        boton_buscar_rapido.grid(
            row=0,
            column=1,
            sticky="e",
        )

        def actualizar_estado_busqueda(*_args):
            valor = valor_busqueda_rapida.get().strip()
            habilitado = (
                len(valor) >= 2
                and self.validar_entrada_busqueda(valor)
            )
            boton_buscar_rapido.configure(
                state=(tk.NORMAL if habilitado else tk.DISABLED),
                bg=(COLOR_ROJO if habilitado else COLOR_PANEL_CLARO),
                fg=(COLOR_BLANCO if habilitado else COLOR_GRIS),
            )
            limpiar_mensaje_busqueda()

        valor_busqueda_rapida.trace_add(
            "write",
            actualizar_estado_busqueda,
        )

        def resaltar_boton_buscar(_evento):
            if boton_buscar_rapido["state"] != tk.DISABLED:
                boton_buscar_rapido.configure(bg=COLOR_ROJO_CLARO)

        def restaurar_boton_buscar(_evento):
            habilitado = boton_buscar_rapido["state"] != tk.DISABLED
            boton_buscar_rapido.configure(
                bg=(COLOR_ROJO if habilitado else COLOR_PANEL_CLARO),
            )

        boton_buscar_rapido.bind(
            "<Enter>",
            resaltar_boton_buscar,
        )
        boton_buscar_rapido.bind(
            "<Leave>",
            restaurar_boton_buscar,
        )
        entrada_busqueda_rapida.bind("<Return>", buscar_rapido)
        entrada_busqueda_rapida.focus_set()


