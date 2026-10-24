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




class EnfermeriaInicioMixin:

    def _citas_asignadas(self):
        return sorted(
            (
                cita
                for cita in self.sistema.obtener_citas()
                if cita.profesional.codigo_profesional
                == self.enfermero_actual.codigo_profesional
                and cita.estado not in {"Cancelada", "No atendida"}
            ),
            key=lambda cita: cita.fecha_hora,
        )
    def mostrar_inicio(self):
        citas = self._citas_asignadas()
        farmacia = self.sistema.obtener_estadisticas_medicamentos()
        disponibles = self.sistema.obtener_medicamentos_disponibles()
        contenido = self._iniciar_pantalla(
            "Portal de Enfermería",
            f"{self.enfermero_actual.nombre} · Código "
            f"{self.enfermero_actual.codigo_profesional}",
        )

        tk.Label(
            contenido,
            text="Resumen de hoy",
            font=("Arial", 15, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(anchor="w", pady=(0, 8))
        self._crear_estadisticas(
            contenido,
            (
                (len(citas), "citas asignadas"),
                (farmacia["unidades_disponibles"], "unidades disponibles"),
                (farmacia["ventas_hoy"], "ventas registradas hoy"),
            ),
        )

        tk.Label(
            contenido,
            text="MÓDULOS DE ENFERMERÍA",
            font=("Arial", 14, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(anchor="w", pady=(0, 4))
        modulos = tk.Frame(contenido, bg=COLOR_FONDO)
        modulos.pack(fill="x", pady=(0, 14))
        modulos.columnconfigure(0, weight=1, uniform="modulos_enfermeria")
        modulos.columnconfigure(1, weight=1, uniform="modulos_enfermeria")
        self._crear_modulo(
            modulos,
            0,
            0,
            "＋",
            "Registrar medicamentos",
            "",
            self.mostrar_registro_medicamentos,
        )
        self._crear_modulo(
            modulos,
            0,
            1,
            "▤",
            "Medicamentos disponibles",
            "",
            self.mostrar_medicamentos_disponibles,
        )
        self._crear_modulo(
            modulos,
            1,
            0,
            "S/",
            "Registrar venta",
            "",
            self.mostrar_ventas,
        )
        self._crear_modulo(
            modulos,
            1,
            1,
            "◷",
            "Agenda asignada",
            "",
            self.mostrar_agenda,
        )

        panel = self._tarjeta(contenido, "Agenda asignada")
        panel.pack(fill="x", pady=(0, 12))
        if not citas:
            tk.Label(
                panel,
                text="No hay citas asignadas en este momento.",
                font=("Arial", 10),
                fg=COLOR_GRIS,
                bg=COLOR_PANEL,
            ).pack(anchor="w", pady=4)
        else:
            for cita in citas:
                fila = tk.Frame(panel, bg=COLOR_PANEL, padx=2, pady=8)
                fila.pack(fill="x")
                fila.columnconfigure(0, weight=1)
                fila.columnconfigure(1, weight=2)
                fila.columnconfigure(2, weight=1)
                tk.Label(
                    fila,
                    text=f"{cita.fecha} · {cita.hora}",
                    font=("Arial", 10, "bold"),
                    fg=COLOR_TEXTO,
                    bg=COLOR_PANEL,
                    anchor="w",
                ).grid(row=0, column=0, sticky="ew", padx=5)
                tk.Label(
                    fila,
                    text=f"{cita.paciente.nombre}\n{cita.motivo}",
                    font=("Arial", 10),
                    fg=COLOR_TEXTO,
                    bg=COLOR_PANEL,
                    anchor="w",
                    justify="left",
                    wraplength=420,
                ).grid(row=0, column=1, sticky="ew", padx=5)
                tk.Label(
                    fila,
                    text=cita.estado,
                    font=("Arial", 9, "bold"),
                    fg=COLOR_ROJO,
                    bg=COLOR_PANEL,
                    anchor="e",
                ).grid(row=0, column=2, sticky="ew", padx=5)
                tk.Frame(panel, bg=COLOR_PANEL_CLARO, height=1).pack(fill="x")

