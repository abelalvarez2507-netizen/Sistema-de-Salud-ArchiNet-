import pytest

from interfaz.pantalla_paciente import PantallaPaciente, SINTOMAS_CITA
from servicios.validaciones import validar_motivo


class ValorSeleccion:
    def __init__(self, valor):
        self.valor = valor

    def get(self):
        return self.valor


class EntradaTexto:
    def __init__(self, texto):
        self.texto = texto

    def get(self):
        return self.texto


def test_motivo_acepta_varios_sintomas_y_otro_sintoma():
    selecciones = [
        (sintoma, ValorSeleccion(True))
        for sintoma in SINTOMAS_CITA
    ]

    motivo = PantallaPaciente._obtener_motivo_sintomas(
        selecciones,
        EntradaTexto("Tos nocturna"),
    )

    assert all(sintoma in motivo for sintoma in SINTOMAS_CITA)
    assert "Tos nocturna" in motivo
    assert validar_motivo(motivo) == motivo


def test_motivo_requiere_un_sintoma():
    selecciones = [
        (sintoma, ValorSeleccion(False))
        for sintoma in SINTOMAS_CITA
    ]

    with pytest.raises(ValueError, match="al menos un síntoma"):
        PantallaPaciente._obtener_motivo_sintomas(
            selecciones,
            EntradaTexto("  "),
        )
