"""Valoración inicial registrada por el personal de triaje."""

import math
import re
from datetime import datetime

from servicios.validaciones import validar_codigo


class ValoracionTriaje:
    NIVELES = {
        1: ("Rojo", "Inmediata", 0),
        2: ("Naranja", "Muy urgente · 10 a 15 minutos", 15),
        3: ("Amarillo", "Urgente · 30 a 60 minutos", 60),
        4: ("Verde", "Menor urgencia · hasta 3 horas", 180),
        5: ("Azul", "No urgente · hasta 4 horas", 240),
    }

    def __init__(
        self,
        cita_codigo,
        enfermero_codigo,
        temperatura,
        presion_arterial,
        frecuencia_cardiaca,
        saturacion_oxigeno,
        peso,
        talla,
        nivel,
        cita_medica_codigo=None,
        fuera_plazo=False,
        fecha_registro=None,
    ):
        self.cita_codigo = validar_codigo(cita_codigo, "El código de la cita de triaje")
        self.enfermero_codigo = validar_codigo(enfermero_codigo, "El código del técnico de triaje")
        self.temperatura = self._numero(temperatura, "La temperatura", maximo=100)
        self.presion_arterial = str(presion_arterial or "").strip()
        if not re.fullmatch(r"\d{2,3}\s*/\s*\d{2,3}", self.presion_arterial):
            raise ValueError("La presión arterial debe escribirse como sistólica/diastólica, por ejemplo 120/80.")
        self.frecuencia_cardiaca = self._numero(frecuencia_cardiaca, "La frecuencia cardíaca")
        self.saturacion_oxigeno = self._numero(saturacion_oxigeno, "La saturación de oxígeno", maximo=100)
        self.peso = self._numero(peso, "El peso")
        self.talla = self._numero(talla, "La talla", maximo=300)
        if isinstance(nivel, bool) or int(nivel) not in self.NIVELES:
            raise ValueError("Selecciona un nivel de urgencia del 1 al 5.")
        self.nivel = int(nivel)
        self.cita_medica_codigo = (
            validar_codigo(cita_medica_codigo, "El código de la cita médica")
            if cita_medica_codigo
            else None
        )
        self.fuera_plazo = bool(fuera_plazo)
        self.fecha_registro = fecha_registro or datetime.now()
        if isinstance(self.fecha_registro, str):
            self.fecha_registro = datetime.fromisoformat(self.fecha_registro)

    @staticmethod
    def _numero(valor, etiqueta, maximo=None):
        try:
            numero = float(str(valor).replace(",", ".").strip())
        except (TypeError, ValueError) as error:
            raise ValueError(f"{etiqueta} debe ser un número válido.") from error
        if not math.isfinite(numero) or numero <= 0 or (maximo and numero > maximo):
            raise ValueError(f"{etiqueta} está fuera del rango permitido.")
        return numero

    @property
    def color(self):
        return self.NIVELES[self.nivel][0]

    @property
    def nombre_nivel(self):
        return self.NIVELES[self.nivel][1]

    @property
    def plazo_minutos(self):
        return self.NIVELES[self.nivel][2]
