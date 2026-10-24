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




class EnfermeriaSesionMixin:

    def cerrar_sesion(self):
        try:
            self.sistema.cerrar()
        except Exception:
            pass
        self.pantalla_inicio.mostrar()

