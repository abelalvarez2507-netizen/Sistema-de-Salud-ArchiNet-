"""Agenda y valoración de citas regulares en el área de triaje."""

import tkinter as tk
from tkinter import messagebox

from interfaz.estilos import (
    COLOR_BLANCO,
    COLOR_FONDO,
    COLOR_GRIS,
    COLOR_PANEL,
    COLOR_PANEL_CLARO,
    COLOR_ROJO,
    COLOR_TEXTO,
    FUENTE_BOTON,
    FUENTE_LOGO,
    FUENTE_SUBTITULO,
    FUENTE_TITULO,
)
from interfaz.navegacion import VistaDesplazable, instalar_navegacion
from servicios.sistema_salud import SistemaSalud


COLORES_NIVEL = {
    1: "#B42318",
    2: "#E87500",
    3: "#D6A900",
    4: "#2F8F4E",
    5: "#2878C7",
}


class PantallaTriaje:
    """Permite al personal técnico registrar signos vitales y prioridad."""

    def __init__(self, ventana, pantalla_inicio, sesion):
        if sesion is None or sesion.rol != "triaje":
            raise ValueError("Se requiere una sesión de triaje autenticada.")
        self.ventana = ventana
        self.pantalla_inicio = pantalla_inicio
        self.sesion = sesion
        self.sistema = SistemaSalud()
        personal = self.sistema.buscar_personal_por_codigo(sesion.codigo_referencia or "")
        if not personal or personal[0] not in self.sistema.obtener_personal_triaje():
            self.sistema.cerrar()
            raise ValueError("La cuenta ya no está vinculada a personal de triaje activo.")
        self.enfermero_actual = personal[0]
        self.ventana.title("Archinet - Área de Triaje")
        self.ventana.configure(bg=COLOR_FONDO)
        self.mostrar_inicio()

    def cerrar_sesion(self):
        self.sistema.cerrar()
        self.pantalla_inicio.mostrar()

    def cambiar_area(self):
        self.pantalla_inicio.mostrar_selector_enfermeria()

    def _contenido(self, titulo, volver):
        for widget in self.ventana.winfo_children():
            try:
                widget.destroy()
            except tk.TclError:
                pass
        instalar_navegacion(
            self.ventana,
            volver=volver,
            inicio=self.cerrar_sesion,
        )
        vista = VistaDesplazable(self.ventana, COLOR_FONDO)
        vista.pack(fill="both", expand=True)
        contenido = vista.contenido
        contenido.configure(padx=24, pady=18)
        barra = tk.Frame(contenido, bg=COLOR_FONDO)
        barra.pack(fill="x", pady=(0, 12))
        tk.Button(
            barra,
            text="↔  Cambiar de área",
            command=self.cambiar_area,
            font=FUENTE_BOTON,
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=8,
        ).pack(side="left")
        tk.Button(
            barra,
            text="Cerrar sesión",
            command=self.cerrar_sesion,
            font=FUENTE_BOTON,
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=8,
        ).pack(side="right")
        tk.Label(
            barra,
            text="ARCHINET",
            font=FUENTE_LOGO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(side="right", padx=(0, 18))
        tk.Frame(contenido, bg=COLOR_ROJO, height=3).pack(fill="x", pady=(0, 24))
        tk.Label(
            contenido,
            text=titulo,
            font=FUENTE_TITULO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(anchor="w", pady=(0, 6))
        tk.Label(
            contenido,
            text=f"Sesión iniciada · {self.sesion.usuario}",
            font=FUENTE_SUBTITULO,
            fg=COLOR_GRIS,
            bg=COLOR_FONDO,
        ).pack(anchor="w")
        return contenido

    def mostrar_inicio(self):
        contenido = self._contenido("Agenda de triaje", self.mostrar_inicio)
        tk.Label(
            contenido,
            text="Citas regulares pendientes de valoración",
            font=FUENTE_SUBTITULO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(anchor="w", pady=(20, 8))
        citas = self.sistema.obtener_citas_triaje_pendientes(
            self.enfermero_actual.codigo_profesional
        )
        if not citas:
            tk.Label(
                contenido,
                text="No hay citas de triaje pendientes.",
                font=FUENTE_BOTON,
                fg=COLOR_GRIS,
                bg=COLOR_FONDO,
            ).pack(anchor="w", pady=12)
            return
        for cita in citas:
            tarjeta = tk.Frame(contenido, bg=COLOR_PANEL, padx=18, pady=14)
            tarjeta.pack(fill="x", pady=6)
            tk.Label(
                tarjeta,
                text=f"{cita.fecha} · {cita.hora} · {cita.paciente.nombre}",
                font=("Arial", 14, "bold"),
                fg=COLOR_TEXTO,
                bg=COLOR_PANEL,
            ).pack(anchor="w")
            tk.Label(
                tarjeta,
                text=f"Motivo: {cita.motivo}",
                font=("Arial", 11),
                fg=COLOR_TEXTO,
                bg=COLOR_PANEL,
                wraplength=900,
                justify="left",
            ).pack(anchor="w", pady=(4, 10))
            tk.Button(
                tarjeta,
                text="Registrar signos vitales y urgencia",
                command=lambda item=cita: self.mostrar_valoracion(item),
                font=FUENTE_BOTON,
                bg=COLOR_ROJO,
                fg=COLOR_BLANCO,
                relief="flat",
                cursor="hand2",
                padx=14,
                pady=8,
            ).pack(anchor="w")

    def mostrar_valoracion(self, cita):
        contenido = self._contenido(
            f"Valoración de {cita.paciente.nombre}",
            self.mostrar_inicio,
        )
        tk.Label(
            contenido,
            text=f"Cita de triaje · {cita.fecha} a las {cita.hora} · Motivo: {cita.motivo}",
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            wraplength=1050,
            justify="left",
        ).pack(anchor="w", pady=(18, 12))
        formulario = tk.Frame(contenido, bg=COLOR_PANEL, padx=18, pady=16)
        formulario.pack(fill="x", pady=6)
        campos = (
            ("Temperatura (°C)", "temperatura"),
            ("Presión arterial (sistólica/diastólica)", "presion"),
            ("Frecuencia cardíaca (latidos por minuto)", "frecuencia"),
            ("Saturación de oxígeno (%)", "saturacion"),
            ("Peso (kg)", "peso"),
            ("Talla (cm)", "talla"),
        )
        entradas = {}
        for fila, (etiqueta, clave) in enumerate(campos):
            tk.Label(
                formulario,
                text=etiqueta,
                font=FUENTE_BOTON,
                fg=COLOR_TEXTO,
                bg=COLOR_PANEL,
            ).grid(row=fila, column=0, sticky="w", padx=(0, 14), pady=5)
            entrada = tk.Entry(
                formulario,
                width=24,
                bg=COLOR_PANEL_CLARO,
                fg=COLOR_TEXTO,
                insertbackground=COLOR_TEXTO,
                relief="flat",
            )
            entrada.grid(row=fila, column=1, sticky="w", pady=5, ipady=5)
            entradas[clave] = entrada

        tk.Label(
            formulario,
            text="Nivel de urgencia asignado por el técnico",
            font=FUENTE_BOTON,
            fg=COLOR_TEXTO,
            bg=COLOR_PANEL,
        ).grid(row=len(campos), column=0, columnspan=2, sticky="w", pady=(18, 8))
        nivel_var = tk.IntVar(value=0)
        niveles = (
            (1, "Nivel 1 · Rojo\nInmediata"),
            (2, "Nivel 2 · Naranja\n10–15 minutos"),
            (3, "Nivel 3 · Amarillo\n30–60 minutos"),
            (4, "Nivel 4 · Verde\nHasta 3 horas"),
            (5, "Nivel 5 · Azul\nHasta 4 horas"),
        )
        panel_niveles = tk.Frame(formulario, bg=COLOR_PANEL)
        panel_niveles.grid(row=len(campos) + 1, column=0, columnspan=2, sticky="ew")
        for columna, (nivel, etiqueta) in enumerate(niveles):
            tk.Radiobutton(
                panel_niveles,
                text=etiqueta,
                variable=nivel_var,
                value=nivel,
                font=("Arial", 10, "bold"),
                fg=COLOR_BLANCO,
                bg=COLORES_NIVEL[nivel],
                selectcolor=COLORES_NIVEL[nivel],
                activebackground=COLORES_NIVEL[nivel],
                activeforeground=COLOR_BLANCO,
                indicatoron=False,
                width=19,
                height=3,
                wraplength=145,
                relief="flat",
                cursor="hand2",
            ).grid(row=0, column=columna, padx=4, pady=3, sticky="ew")
            panel_niveles.columnconfigure(columna, weight=1)

        def guardar():
            try:
                if nivel_var.get() not in {1, 2, 3, 4, 5}:
                    raise ValueError("Selecciona el nivel de urgencia de la atención.")
                cita_medica, cita_movida, valoracion = self.sistema.registrar_valoracion_triaje(
                    cita,
                    self.enfermero_actual,
                    entradas["temperatura"].get(),
                    entradas["presion"].get(),
                    entradas["frecuencia"].get(),
                    entradas["saturacion"].get(),
                    entradas["peso"].get(),
                    entradas["talla"].get(),
                    nivel_var.get(),
                )
                mensaje = (
                    f"Nivel {valoracion.nivel} · {valoracion.color}. "
                    f"Consulta con medicina general: {cita_medica.fecha} a las {cita_medica.hora} "
                    f"con {cita_medica.profesional.nombre}."
                )
                if cita_movida:
                    mensaje += (
                        f"\nSe reprogramó la cita ordinaria de {cita_movida.paciente.nombre} "
                        f"al {cita_movida.fecha} a las {cita_movida.hora}."
                    )
                if valoracion.fuera_plazo:
                    mensaje += "\nEl primer horario libre excede el tiempo objetivo; revise la prioridad de atención."
                messagebox.showinfo("Triaje registrado", mensaje, parent=self.ventana)
                self.mostrar_inicio()
            except (TypeError, ValueError) as error:
                messagebox.showerror("No se pudo registrar el triaje", str(error), parent=self.ventana)

        tk.Button(
            contenido,
            text="Guardar valoración y agendar médico general",
            command=guardar,
            font=FUENTE_BOTON,
            bg=COLOR_ROJO,
            fg=COLOR_BLANCO,
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=10,
        ).pack(anchor="w", pady=(12, 20))
