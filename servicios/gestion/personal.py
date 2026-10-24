from modelos.herencia.paciente import Paciente
from modelos.agenda.cita import Cita
from modelos.herencia.personal_salud import PersonalSalud
from modelos.atenciones.atencion_medica import AtencionMedica
from modelos.atenciones.medicamento_recetado import MedicamentoRecetado
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import random

from servicios.persistencia.repositorio import RepositorioSalud
from servicios.fabricacion.fabrica import FabricaEntidades
from servicios.persistencia.contratos import RepositorioSaludProtocol




class SistemaPersonalMixin:

    def _cargar_personal(self):

        datos = (
            self._repositorio
            .obtener_personal()
        )

        self._personal = [

            FabricaEntidades
            .crear_personal_desde_datos_protegidos(
                codigo_profesional,
                dni_hash,
                dni_salt,
                nombre,
                edad,
                especialidad
            )

            for (
                codigo_profesional,
                dni_hash,
                dni_salt,
                nombre,
                edad,
                especialidad
            ) in datos
        ]
    def generar_codigo_personal(self, prefijo):
        """Devuelve el siguiente código libre para un prefijo, sin tope de cifras."""
        prefijo = str(prefijo or "").strip().upper()
        if not prefijo.isalpha():
            raise ValueError("El prefijo del código de personal no es válido.")
        ocupados = set()
        for persona in self._personal:
            codigo = persona.codigo_personal.upper()
            if codigo.startswith(prefijo) and codigo[len(prefijo):].isdigit():
                ocupados.add(int(codigo[len(prefijo):]))
        numero = 1
        while numero in ocupados:
            numero += 1
        return f"{prefijo}{numero:03d}"
    def registrar_personal(
        self,
        profesional,
    ):

        if not isinstance(
            profesional,
            PersonalSalud
        ):
            raise TypeError(
                "El registro debe ser "
                "un objeto PersonalSalud."
            )

        existe_codigo = any(
            existente.codigo_profesional
            == profesional.codigo_profesional
            for existente in self._personal
        )

        if existe_codigo:
            raise ValueError(
                "Ya existe un profesional "
                "con ese código."
            )

        if self._repositorio.existe_dni_personal(
            profesional.dni
        ):
            raise ValueError(
                "Ya existe un profesional "
                "con ese DNI."
            )

        self._repositorio.guardar_personal(
            profesional
        )

        self._personal.append(
            profesional
        )
    def obtener_personal(self):
        return list(self._personal)
    def buscar_personal_por_codigo(
        self,
        codigo
    ):

        codigo = codigo.strip()

        return list(
            filter(
                lambda profesional:
                    (
                        profesional.codigo_profesional
                        .lower()
                        == codigo.lower()
                    ),
                self._personal
            )
        )
    def buscar_personal_por_dni(
        self,
        dni
    ):
        """Busca profesionales verificando el DNI contra su huella protegida."""

        dni = str(dni).strip()

        return list(
            filter(
                lambda profesional:
                    profesional.verificar_dni(dni),
                self._personal
            )
        )
    def total_personal(self):
        return len(self._personal)

