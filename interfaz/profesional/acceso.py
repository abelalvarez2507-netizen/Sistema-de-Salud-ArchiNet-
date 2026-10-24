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




class ProfesionalAccesoMixin:

    def mostrar_acceso(self):
        contenedor = self._marco_base(
            "Acceso del profesional",
            "Ingresa tu código profesional o DNI.",
        )
        tarjeta = tk.Frame(contenedor, bg=COLOR_PANEL, padx=28, pady=24)
        tarjeta.pack(pady=24)
        tk.Label(
            tarjeta,
            text="Código profesional o DNI",
            font=FUENTE_SECCION,
            fg=COLOR_TEXTO,
            bg=COLOR_PANEL,
        ).pack(pady=(0, 12))
        self.entrada_identificacion = tk.Entry(
            tarjeta,
            width=28,
            font=("Arial", 14),
            justify="center",
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="flat",
        )
        self.entrada_identificacion.pack(ipady=8)
        validacion = self.ventana.register(self._validar_identificacion)
        self.entrada_identificacion.configure(
            validate="key",
            validatecommand=(validacion, "%P"),
        )
        self._boton(tarjeta, "Ingresar", self.autenticar).pack(pady=(15, 0))
        tk.Label(
            tarjeta,
            text="Por seguridad, el DNI no se muestra por completo después de la autenticación.",
            font=("Arial", 9),
            fg=COLOR_GRIS,
            bg=COLOR_PANEL,
            justify="center",
            wraplength=380,
        ).pack(pady=(12, 0))
        self.entrada_identificacion.bind(
            "<Return>",
            lambda evento: self.autenticar(),
        )
        self.entrada_identificacion.focus_set()
    @staticmethod
    def _validar_identificacion(valor):
        return all(
            caracter.isalnum() or caracter in "-_" for caracter in valor
        )
    def autenticar(self):
        if self.profesional_actual is not None:
            return
        valor = self.entrada_identificacion.get().strip()
        if not valor:
            messagebox.showwarning("Dato requerido", "Ingresa tu código o DNI.")
            return
        if valor.isdigit() and len(valor) == 8:
            profesionales = self.sistema.buscar_personal_por_dni(valor)
        elif self._validar_identificacion(valor) and len(valor) >= 2:
            profesionales = self.sistema.buscar_personal_por_codigo(valor)
        else:
            profesionales = []
        if not profesionales:
            messagebox.showerror(
                "Acceso no autorizado",
                "No se encontró un profesional registrado con ese código o DNI.",
            )
            return
        self.profesional_actual = profesionales[0]
        self.mostrar_agenda()

