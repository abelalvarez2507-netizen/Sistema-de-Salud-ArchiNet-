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




class SistemaPacientesMixin:

    def _cargar_pacientes(self):

        datos = (
            self._repositorio
            .obtener_pacientes()
        )

        self._pacientes = [

            FabricaEntidades
            .crear_paciente_desde_datos_protegidos(
                codigo,
                dni_hash,
                dni_salt,
                nombre,
                edad
            )

            for (
                codigo,
                dni_hash,
                dni_salt,
                nombre,
                edad
            ) in datos
        ]
    def generar_codigo_paciente(self):

        numeros_ocupados = set()

        for paciente in self._pacientes:

            codigo = paciente.codigo.upper()

            if codigo.startswith("P"):

                try:
                    numero = int(codigo[1:])
                    numeros_ocupados.add(numero)

                except ValueError:
                    continue

        numero = 1

        while numero in numeros_ocupados:
            numero += 1

        return f"P{numero:03d}"
    def registrar_paciente(self, paciente):

        if not isinstance(
            paciente,
            Paciente
        ):
            raise TypeError(
                "El registro debe ser "
                "un objeto Paciente."
            )

        existe_codigo = any(
            existente.codigo == paciente.codigo
            for existente in self._pacientes
        )

        if existe_codigo:
            raise ValueError(
                "Ya existe un paciente "
                "con ese código."
            )

        if self._repositorio.existe_dni_paciente(
            paciente.dni
        ):
            raise ValueError(
                "Ya existe un paciente "
                "con ese DNI."
            )

        self._repositorio.guardar_paciente(
            paciente
        )

        self._pacientes.append(
            paciente
        )
    def obtener_pacientes(self):
        return list(self._pacientes)
    def buscar_paciente_por_codigo(
        self,
        codigo
    ):

        codigo = codigo.strip()

        return list(
            filter(
                lambda paciente:
                    paciente.codigo.lower()
                    == codigo.lower(),
                self._pacientes
            )
        )
    def buscar_paciente_por_dni(
        self,
        dni
    ):
        """Busca pacientes verificando el DNI contra su huella protegida."""

        dni = str(dni).strip()

        return list(
            filter(
                lambda paciente:
                    paciente.verificar_dni(dni),
                self._pacientes
            )
        )
    def buscar_pacientes_por_edad(
        self,
        edad_minima
    ):

        return list(
            filter(
                lambda paciente:
                    paciente.edad >= edad_minima,
                self._pacientes
            )
        )
    def obtener_historial_paciente(
        self,
        codigo_paciente
    ):

        paciente = next(
            (
                paciente
                for paciente in self._pacientes
                if paciente.codigo
                == codigo_paciente
            ),
            None
        )

        if paciente is None:
            raise ValueError(
                "No se encontró el paciente."
            )

        atenciones_por_cita = {
            atencion.cita.codigo: atencion for atencion in self._atenciones
        }
        citas = list(
            filter(
                lambda cita:
                    (
                        cita.paciente.codigo
                        == codigo_paciente
                    )
                    and
                    (
                        cita.estado == "Atendida"
                        or (
                            atenciones_por_cita.get(cita.codigo)
                            and atenciones_por_cita[cita.codigo].profesional_derivado
                        )
                    ),
                self._citas
            )
        )

        atenciones = list(
            filter(
                lambda atencion:
                    (
                        atencion.cita.paciente.codigo
                        == codigo_paciente
                    )
                    and
                    (
                        atencion.estado == "Finalizada"
                        or atencion.profesional_derivado is not None
                    ),
                self._atenciones
            )
        )

        return {
            "paciente": paciente,
            "citas": citas,
            "atenciones": atenciones,
            "ventas_medicamentos": (
                self._repositorio.obtener_ventas_paciente(paciente.codigo)
                if hasattr(self._repositorio, "obtener_ventas_paciente")
                else []
            ),
        }
    def total_pacientes(self):
        return len(self._pacientes)

