
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



class AdministrativoFormulariosMixin:

    def actualizar_dashboard(self):

        for widget in self.ventana.winfo_children():

            try:
                widget.destroy()
            except tk.TclError:
                pass

        self._pantalla_actual = None
        self._pantalla_principal = None

        self.crear_interfaz()

    def validar_dni(
        self,
        dni
    ):

        return validar_dni_valor(
            dni
        )

    def crear_campo_dni(
        self,
        ventana
    ):

        marco = tk.Frame(
            ventana
        )

        marco.pack(
            pady=5
        )

        tk.Label(
            marco,
            text="DNI:"
        ).pack()

        entrada = tk.Entry(
            marco,
            width=35
        )

        entrada.pack()

        validacion = ventana.register(
            validar_dni_en_edicion
        )

        entrada.config(
            validate="key",
            validatecommand=(
                validacion,
                "%P"
            )
        )

        return entrada

    def validar_entrada_busqueda(
        self,
        nuevo_valor,
        maximo=None
    ):

        if nuevo_valor == "":
            return True

        return (maximo is None or len(nuevo_valor) <= maximo) and all(
            caracter.isalnum() or caracter in "-_"
            for caracter in nuevo_valor
        )

    def configurar_limite_busqueda(
        self,
        entrada,
        ventana=None,
        maximo=None
    ):

        registro = (
            ventana
            if ventana is not None
            else self.ventana
        )

        validacion = registro.register(
            lambda valor:
            self.validar_entrada_busqueda(
                valor,
                maximo
            )
        )

        entrada.config(
            validate="key",
            validatecommand=(
                validacion,
                "%P"
            )
        )

        return entrada

    def crear_campo_fecha(
        self,
        ventana
    ):

        marco = tk.Frame(
            ventana
        )

        marco.pack(
            pady=5
        )

        entrada = tk.Entry(
            marco,
            width=25,
            fg="gray"
        )

        entrada.pack()

        entrada.insert(
            0,
            "DD/MM/AAAA"
        )

        entrada.placeholder_texto = "DD/MM/AAAA"
        entrada.placeholder_activo = True

        def entrar(evento):

            if entrada.placeholder_activo:

                entrada.delete(
                    0,
                    tk.END
                )

                entrada.config(
                    fg="black"
                )

                entrada.placeholder_activo = False

        def salir(evento):

            if not entrada.get():

                entrada.insert(
                    0,
                    "DD/MM/AAAA"
                )

                entrada.config(
                    fg="gray"
                )

                entrada.placeholder_activo = True


        entrada.bind(
            "<FocusIn>",
            entrar
        )

        entrada.bind(
            "<FocusOut>",
            salir
        )

        return configurar_mascara_fecha(entrada)

    def validar_fecha(
        self,
        fecha
    ):

        try:

            fecha = fecha.strip()

            fecha_convertida = datetime.strptime(
                fecha,
                "%d/%m/%Y"
            )

        except ValueError:

            raise ValueError(
                "La fecha debe tener el formato "
                "DD/MM/AAAA y ser una fecha válida."
            )

        if fecha_convertida.date() < datetime.now().date():
            raise ValueError(
                "La fecha de la cita no puede ser anterior a hoy."
            )

        return True

    def crear_selector_horarios(
        self,
        contenedor,
        profesional_var,
        entrada_fecha,
        excluir_codigo=None,
    ):
        tk.Label(
            contenedor,
            text="Horarios disponibles (turnos de 30 minutos, 07:00–18:00; último inicio 17:30):",
            font=FUENTE_NORMAL_BOLD,
        ).pack(pady=(8, 4))
        hora_var = tk.StringVar(value="")
        selector = tk.OptionMenu(contenedor, hora_var, "")
        selector.configure(cursor="hand2")
        selector.pack()

        def actualizar(event=None):
            codigo = profesional_var.get().split(" - ")[0]
            fecha = entrada_fecha.get().strip()
            if getattr(entrada_fecha, "placeholder_activo", False):
                fecha = ""
            try:
                self.validar_fecha(fecha)
                horarios = self.sistema.horarios_disponibles(
                    codigo,
                    fecha,
                    excluir_codigo=excluir_codigo,
                )
            except ValueError:
                horarios = []
            menu = selector["menu"]
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
                    label="Ingresa una fecha futura con turnos libres",
                    command=lambda: None,
                )
                hora_var.set("")

        entrada_fecha.bind("<FocusOut>", actualizar, add="+")
        entrada_fecha.bind("<Return>", actualizar, add="+")
        profesional_var.trace_add("write", lambda *_args: actualizar())
        return hora_var, actualizar

    def generar_codigo_profesional(self):
        return self.sistema.generar_codigo_personal("CMP")

    def generar_codigo_enfermeria(self):
        return self.sistema.generar_codigo_personal("MTF")

