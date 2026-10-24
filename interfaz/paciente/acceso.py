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




class PacienteAccesoMixin:

    def autenticar_paciente(self):

        # La identidad se valida en el modal de acceso, antes de abrir el
        # portal. La sesión actual no puede cambiarse desde esta pantalla.
        if self.paciente_actual is not None:
            return

        valor = self.campo_dni.get().strip()

        if not valor:

            messagebox.showwarning(
                "Dato requerido",
                "Ingresa tu código o DNI."
            )

            return

        es_dni = valor.isdigit() and len(valor) == 8
        tipo = "DNI" if es_dni else "Código"
        self.tipo_busqueda.set(tipo)

        if es_dni:
            try:
                valor = validar_dni_valor(valor)
            except ValueError as error:
                messagebox.showerror("DNI inválido", str(error))
                return
        else:
            if (
                not self._validar_busqueda_tecla(valor)
                or len(valor) < 2
            ):

                messagebox.showerror(
                    "Código inválido",
                    "El código debe tener 2 o más letras, números, "
                    "guiones o guiones bajos."
                )

                return

        if es_dni:
            pacientes = (
                self.sistema
                .buscar_paciente_por_dni(valor)
            )
        else:
            pacientes = (
                self.sistema
                .buscar_paciente_por_codigo(valor)
            )

        if not pacientes:

            self.paciente_actual = None

            tipo_nombre = "DNI" if tipo == "DNI" else "código"

            self.etiqueta_sesion.configure(
                text=(
                    "No se encontró un paciente con ese "
                    f"{tipo_nombre}."
                ),
                fg=COLOR_ERROR
            )

            messagebox.showerror(
                "Acceso no autorizado",
                "No se encontró un paciente "
                f"registrado con ese {tipo_nombre}."
            )

            return

        self.paciente_actual = pacientes[0]

        self.etiqueta_sesion.configure(
            text=(
                "Paciente identificado: "
                f"{self.paciente_actual.nombre}"
            ),
            fg=COLOR_TEXTO
        )

        self.campo_dni.delete(
            0,
            tk.END
        )

        messagebox.showinfo(
            "Acceso correcto",
            "Paciente autenticado correctamente."
        )
    def paciente_autenticado(self):

        if self.paciente_actual is None:

            messagebox.showwarning(
                "Acceso requerido",
                "Primero debes ingresar tu código o DNI "
                "para consultar esta información."
            )

            self.campo_dni.focus_set()

            return False

        return True

