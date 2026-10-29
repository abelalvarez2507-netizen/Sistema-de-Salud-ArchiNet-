"""Autenticación por rol para los portales de Archinet."""

from dataclasses import dataclass, field
import hashlib
import hmac
import os
import re
import unicodedata

from servicios.persistencia.repositorio import RepositorioSalud
from servicios.seguridad.seguridad import SeguridadDatos
from servicios.seguridad.almacen_privado import DatosPrivadosUsuario
from servicios.validacion import (
    validar_dni,
    validar_edad,
    validar_especialidad,
    validar_nombre,
)
from modelos.herencia.paciente import Paciente
from modelos.herencia.personal_enfermeria import PersonalEnfermeria
from modelos.herencia.personal_salud import PersonalSalud


@dataclass(frozen=True)
class SesionUsuario:
    """Identidad autenticada que se entrega al portal correspondiente."""

    rol: str
    usuario: str
    codigo_referencia: str | None = None
    datos_privados: object | None = field(default=None, repr=False, compare=False)


from servicios.seguridad.modulos_autenticacion.credenciales import AutenticacionCredencialesMixin
from servicios.seguridad.modulos_autenticacion.registro import AutenticacionRegistroMixin

class ServicioAutenticacion(AutenticacionCredencialesMixin, AutenticacionRegistroMixin):
    ROLES = {"paciente", "administrativa", "profesional", "enfermeria"}
    ITERACIONES_PASSWORD = 310_000
    LONGITUD_SAL = 16
    LONGITUD_HASH = 32
    CODIGO_MEDICO_REGISTRO = "ArchiNet"

    def __init__(self, repositorio=None):
        self.repositorio = repositorio or RepositorioSalud()

    def cerrar(self):
        self.repositorio.cerrar()

    def _crear_sesion(self, rol, usuario, codigo, password):
        datos_privados = None
        if rol == "paciente" and codigo:
            paciente = next(
                (fila for fila in self.repositorio.obtener_pacientes() if fila[0].casefold() == codigo.casefold()),
                None,
            )
            if paciente is None:
                raise ValueError("La cuenta no está vinculada a un paciente registrado.")
            datos_privados = DatosPrivadosUsuario(codigo)
            inicial = {
                "usuario": usuario,
                "perfil": {"codigo": paciente[0], "nombre": paciente[3], "edad": paciente[4]},
                "citas": [],
                "atenciones": [],
                "ventas_medicamentos": [],
            }
            try:
                datos_privados.abrir(password)
            except FileNotFoundError:
                datos_privados.crear(password, inicial)
        return SesionUsuario(rol, usuario, codigo, datos_privados)













