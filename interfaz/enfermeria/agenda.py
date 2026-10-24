"""Portal de enfermería con agenda, inventario y ventas de medicamentos."""

from datetime import date, datetime
import tkinter as tk
from tkinter import ttk

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
    FUENTE_LOGO,
    FUENTE_SUBTITULO,
    FUENTE_TITULO,
)
from interfaz.navegacion import VistaDesplazable, instalar_navegacion
from interfaz.campos import configurar_mascara_fecha
from servicios.seguridad.autenticacion import ServicioAutenticacion
from servicios.gestion.sistema_salud import SistemaSalud


PRODUCTOS_MEDICAMENTO = {
    "Paracetamol": "Paracetamol",
    "Ibuprofeno": "Ibuprofeno",
    "Amoxicilina": "Amoxicilina",
    "Loratadina": "Loratadina",
}

PRINCIPIOS_ACTIVOS = (
    "Paracetamol",
    "Ibuprofeno",
    "Amoxicilina",
    "Loratadina",
    "Ácido acetilsalicílico",
    "Diclofenaco",
    "Naproxeno",
    "Ketorolaco",
    "Amoxicilina + ácido clavulánico",
    "Ampicilina",
    "Azitromicina",
    "Claritromicina",
    "Cefalexina",
    "Ceftriaxona",
    "Ciprofloxacino",
    "Doxiciclina",
    "Eritromicina",
    "Metronidazol",
    "Nitrofurantoína",
    "Sulfametoxazol + trimetoprima",
    "Clindamicina",
    "Cetirizina",
    "Clorfenamina",
    "Omeprazol",
    "Pantoprazol",
    "Metoclopramida",
    "Ondansetrón",
    "Loperamida",
    "Metformina",
    "Glibenclamida",
    "Insulina humana",
    "Enalapril",
    "Losartán",
    "Amlodipino",
    "Hidroclorotiazida",
    "Furosemida",
    "Atorvastatina",
    "Levotiroxina",
    "Salbutamol",
    "Prednisona",
)




class EnfermeriaAgendaMixin:

    def mostrar_agenda(self):
        citas = self._citas_asignadas()
        contenido = self._iniciar_pantalla(
            "Agenda asignada",
            "Citas vinculadas a tu cuenta de enfermería.",
            mostrar_volver=True,
        )
        panel = self._tarjeta(contenido, "Próximas atenciones")
        panel.pack(fill="x")
        if not citas:
            tk.Label(
                panel,
                text="No hay citas asignadas en este momento.",
                font=("Arial", 10),
                fg=COLOR_GRIS,
                bg=COLOR_PANEL,
            ).pack(anchor="w")
            return
        for cita in citas:
            fila = tk.Frame(panel, bg=COLOR_PANEL, pady=14)
            fila.pack(fill="x")
            fila.columnconfigure(0, weight=1)
            fila.columnconfigure(1, weight=2)
            fila.columnconfigure(2, weight=1)
            for col, texto in enumerate(
                (f"{cita.fecha} · {cita.hora}", cita.paciente.nombre, cita.estado)
            ):
                tk.Label(
                    fila,
                    text=texto,
                    font=("Arial", 11, "bold" if col == 2 else "normal"),
                    fg=COLOR_TEXTO,
                    bg=COLOR_PANEL,
                    anchor="w",
                    wraplength=300,
                ).grid(row=0, column=col, sticky="ew", padx=6)
            tk.Label(
                panel,
                text=cita.motivo,
                font=("Arial", 10),
                fg=COLOR_GRIS,
                bg=COLOR_PANEL,
                anchor="w",
                wraplength=850,
                justify="left",
            ).pack(fill="x", padx=6, pady=(0, 5))
            tk.Frame(panel, bg=COLOR_PANEL_CLARO, height=1).pack(fill="x")

