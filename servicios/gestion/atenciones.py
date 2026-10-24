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




class SistemaAtencionesMixin:

    def _cargar_atenciones(self):

        datos = (
            self._repositorio
            .obtener_atenciones()
        )

        for fila in datos:
            codigo, cita_codigo, diagnostico, estado = fila[:4]
            profesional_derivado_codigo = fila[4] if len(fila) > 4 else None
            informe_derivacion = fila[5] if len(fila) > 5 else ""

            cita = next(
                (
                    cita
                    for cita in self._citas
                    if cita.codigo
                    == cita_codigo
                ),
                None
            )

            if cita is None:
                raise ValueError(
                    "Se encontró una atención con "
                    "una cita inexistente."
                )

            recetas = [
                MedicamentoRecetado(medicamento, dias, cada_cuanto)
                for medicamento, dias, cada_cuanto
                in self._repositorio.obtener_recetas_atencion(codigo)
            ] if hasattr(self._repositorio, "obtener_recetas_atencion") else []
            profesional_derivado = next(
                (
                    profesional
                    for profesional in self._personal
                    if profesional.codigo_profesional
                    == profesional_derivado_codigo
                ),
                None,
            )
            atencion = FabricaEntidades.crear_atencion(
                codigo,
                cita,
                diagnostico,
                estado,
                recetas,
                profesional_derivado,
                informe_derivacion,
            )
            self._atenciones.append(atencion)
    def generar_codigo_atencion(self):

        numeros_ocupados = set()

        for atencion in self._atenciones:

            codigo = atencion.codigo.upper()

            if codigo.startswith("A"):

                try:
                    numero = int(codigo[1:])
                    numeros_ocupados.add(numero)

                except ValueError:
                    continue

        numero = 1

        while numero in numeros_ocupados:
            numero += 1

        return f"A{numero:03d}"
    def registrar_atencion(
        self,
        atencion
    ):

        if not isinstance(
            atencion,
            AtencionMedica
        ):
            raise TypeError(
                "El registro debe ser "
                "un objeto AtencionMedica."
            )

        cita = next(
            (
                existente
                for existente in self._citas
                if existente.codigo
                == atencion.cita.codigo
            ),
            None
        )

        if cita is None:
            raise ValueError(
                "La cita no está registrada."
            )

        codigo_existe = any(
            existente.codigo
            == atencion.codigo
            for existente in self._atenciones
        )

        if codigo_existe:
            raise ValueError(
                "Ya existe una atención "
                "con ese código."
            )

        atencion_existente = any(
            existente.cita.codigo
            == cita.codigo
            for existente in self._atenciones
        )

        if atencion_existente:
            raise ValueError(
                "La cita ya tiene una "
                "atención médica registrada."
            )

        self._repositorio.guardar_atencion(
            atencion
        )

        self._atenciones.append(
            atencion
        )

        estado_cita = (
            "No atendida"
            if atencion.estado == "No atendida"
            else "En proceso"
            if atencion.profesional_derivado or atencion.estado != "Finalizada"
            else "Atendida"
        )
        self.actualizar_estado_cita(cita.codigo, estado_cita)
    def actualizar_atencion(
        self,
        codigo_atencion,
        diagnostico,
        recetas=None,
        profesional_derivado=None,
        profesional_autor=None,
    ):
        atencion = next(
            (item for item in self._atenciones if item.codigo == codigo_atencion),
            None,
        )
        if atencion is None:
            raise ValueError("No se encontró la atención médica.")
        atencion.diagnostico = diagnostico
        if profesional_derivado is not None:
            atencion.profesional_derivado = profesional_derivado
        if atencion.profesional_derivado and not atencion.informe_derivacion:
            atencion.informe_derivacion = diagnostico
        self._repositorio.actualizar_diagnostico_atencion(
            codigo_atencion,
            atencion.diagnostico,
            (
                atencion.profesional_derivado.codigo_profesional
                if atencion.profesional_derivado
                else None
            ),
            atencion.informe_derivacion,
        )
        if recetas is not None:
            atencion.recetas = self._validar_recetas(recetas)
            self._repositorio.guardar_recetas_atencion(
                codigo_atencion,
                atencion.recetas,
            )
        es_medico_remitente = (
            atencion.profesional_derivado is not None
            and profesional_autor is not None
            and profesional_autor.codigo_profesional
            == atencion.cita.profesional.codigo_profesional
        )
        self.actualizar_estado_atencion(
            codigo_atencion,
            "En proceso" if es_medico_remitente else "Finalizada",
        )
    def actualizar_estado_atencion(
        self,
        codigo_atencion,
        nuevo_estado
    ):

        if (
            nuevo_estado
            not in AtencionMedica.ESTADOS_VALIDOS
        ):
            raise ValueError(
                "Estado inválido. Use: "
                "Pendiente, En proceso, Finalizada o No atendida."
            )

        atencion = next(
            (
                existente
                for existente in self._atenciones
                if existente.codigo
                == codigo_atencion
            ),
            None
        )

        if atencion is None:
            raise ValueError(
                "No se encontró la atención."
            )

        self._repositorio.actualizar_estado_atencion(
            codigo_atencion,
            nuevo_estado
        )

        atencion.estado = nuevo_estado
        estado_cita = {
            "Pendiente": "Pendiente",
            "En proceso": "En proceso",
            "Finalizada": "Atendida",
            "No atendida": "No atendida",
        }[nuevo_estado]
        self.actualizar_estado_cita(atencion.cita.codigo, estado_cita)
    def obtener_atenciones(self):
        return list(self._atenciones)
    def obtener_atenciones_pendientes(self):

        return list(
            filter(
                lambda atencion:
                    atencion.estado == "Pendiente",
                self._atenciones
            )
        )
    def obtener_atenciones_en_proceso(self):

        return list(
            filter(
                lambda atencion:
                    atencion.estado == "En proceso",
                self._atenciones
            )
        )
    def obtener_atenciones_finalizadas(self):

        return list(
            filter(
                lambda atencion:
                    atencion.estado == "Finalizada",
                self._atenciones
            )
        )
    def total_atenciones(self):
        return len(self._atenciones)
    def total_atenciones_finalizadas(self):
        return len(
            self.obtener_atenciones_finalizadas()
        )

