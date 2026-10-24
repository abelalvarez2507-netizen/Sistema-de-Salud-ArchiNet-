"""Autenticación por rol para los portales de Archinet."""

from dataclasses import dataclass
import hashlib
import hmac
import os
import re
import unicodedata

from servicios.persistencia.repositorio import RepositorioSalud
from servicios.seguridad.seguridad import SeguridadDatos
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




class AutenticacionCredencialesMixin:
    """Operaciones de credenciales para ServicioAutenticacion."""

    def hay_administrador(self):
        return bool(
            self.repositorio.contar_cuentas_acceso("administrativa")
        )
    @staticmethod
    def validar_usuario(usuario):
        usuario = str(usuario or "").strip()
        if not re.fullmatch(r"[A-Za-z0-9._-]{3,32}", usuario):
            raise ValueError(
                "El usuario debe tener entre 3 y 32 caracteres: "
                "letras, números, punto, guion o guion bajo."
            )
        return usuario
    @staticmethod
    def validar_password(password):
        if not isinstance(password, str) or len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        if not any(caracter.isdigit() for caracter in password):
            raise ValueError("La contraseña debe incluir al menos un número.")
        return password
    @classmethod
    def _hash_password(cls, password, sal):
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            sal,
            cls.ITERACIONES_PASSWORD,
            dklen=cls.LONGITUD_HASH,
        )
    @classmethod
    def _proteger_password(cls, password):
        sal = os.urandom(cls.LONGITUD_SAL)
        resumen = cls._hash_password(password, sal)
        return resumen.hex(), sal.hex()
    @classmethod
    def _verificar_password(cls, password, sal_hex, hash_hex):
        try:
            sal = bytes.fromhex(sal_hex)
            esperado = bytes.fromhex(hash_hex)
        except (TypeError, ValueError):
            return False
        obtenido = cls._hash_password(password, sal)
        return hmac.compare_digest(obtenido, esperado)
    def autenticar(self, usuario, password, rol):
        if rol not in self.ROLES or not isinstance(password, str):
            return None
        try:
            usuario = self.validar_usuario(usuario)
        except ValueError:
            return None

        cuenta = self.repositorio.obtener_cuenta_acceso(usuario)
        if cuenta is None:
            # Igualar el coste de una contraseña incorrecta para un usuario
            # inexistente y reducir la enumeración de cuentas por tiempo.
            self._hash_password(password, b"\0" * self.LONGITUD_SAL)
            return None

        nombre, rol_guardado, codigo, resumen, sal, activo = cuenta
        if (
            not activo
            or rol_guardado != rol
            or not self._verificar_password(password, sal, resumen)
        ):
            return None

        if rol == "paciente":
            if not self.repositorio.obtener_datos_paciente_acceso(codigo):
                return None
        elif rol in {"profesional", "enfermeria"}:
            personal = self.repositorio.obtener_datos_personal_acceso(codigo)
            if not personal or not self._puede_entrar(personal[3], rol):
                return None

        return self._crear_sesion(rol, nombre, codigo, password)

