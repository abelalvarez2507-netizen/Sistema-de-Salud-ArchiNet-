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






class SistemaCitasSeguimientoMixin:

    def reprogramar_cita(self, codigo_cita, fecha, hora):
        cita = next(
            (item for item in self._citas if item.codigo == codigo_cita),
            None,
        )
        if cita is None:
            raise ValueError("No se encontró la cita.")
        if cita.estado in {"Atendida", "En proceso", "No atendida", "Cancelada"}:
            raise ValueError("Esta cita ya no se puede reprogramar.")

        from servicios.validacion import normalizar_fecha, normalizar_hora

        fecha_nueva = normalizar_fecha(fecha)
        hora_nueva = normalizar_hora(hora)
        if hora_nueva not in self.HORARIOS_ATENCION:
            raise ValueError(
                "El horario de atención es de 07:00 a 18:00, con turnos cada 30 minutos."
            )
        momento = datetime.strptime(
            f"{fecha_nueva} {hora_nueva}",
            "%d/%m/%Y %H:%M",
        )
        self._validar_fecha_hora_futura(momento)
        self._validar_disponibilidad(
            cita.profesional.codigo_profesional,
            fecha_nueva,
            hora_nueva,
            paciente_codigo=cita.paciente.codigo,
            excluir_codigo=cita.codigo,
        )
        self._repositorio.actualizar_agenda_cita(
            cita.codigo,
            fecha_nueva,
            hora_nueva,
            "Reprogramada",
        )
        cita.fecha = fecha_nueva
        cita.hora = hora_nueva
        cita.estado = "Reprogramada"
    def cancelar_cita(self, codigo_cita):
        self.actualizar_estado_cita(codigo_cita, "Cancelada")
    def actualizar_citas_vencidas(self, ahora=None):
        """Sincroniza automáticamente cita y atención con el turno de 30 minutos."""
        ahora = ahora or datetime.now()
        cambios = 0
        atenciones_por_cita = {
            atencion.cita.codigo: atencion for atencion in self._atenciones
        }

        for cita in self._citas:
            if cita.estado in {"Cancelada", "No atendida"}:
                continue

            atencion = atenciones_por_cita.get(cita.codigo)
            fin_turno = cita.fecha_hora + timedelta(minutes=30)

            if atencion and atencion.estado == "Finalizada":
                if cita.estado != "Atendida":
                    self.actualizar_estado_cita(cita.codigo, "Atendida")
                    cambios += 1
                continue

            if atencion and atencion.estado == "No atendida":
                if cita.estado != "No atendida":
                    self.actualizar_estado_cita(cita.codigo, "No atendida")
                    cambios += 1
                continue

            # Una derivación permanece activa hasta el veredicto del especialista.
            if atencion and atencion.profesional_derivado:
                if cita.fecha_hora > ahora:
                    continue
                if atencion.estado != "En proceso":
                    self.actualizar_estado_atencion(atencion.codigo, "En proceso")
                    cambios += 1
                elif cita.estado != "En proceso":
                    self.actualizar_estado_cita(cita.codigo, "En proceso")
                    cambios += 1
                continue

            if cita.fecha_hora <= ahora < fin_turno:
                if cita.estado != "En proceso":
                    self.actualizar_estado_cita(cita.codigo, "En proceso")
                    cambios += 1
                if atencion and atencion.estado != "En proceso":
                    self.actualizar_estado_atencion(atencion.codigo, "En proceso")
                    cambios += 1
            elif ahora >= fin_turno and cita.estado != "No atendida":
                if atencion:
                    self.actualizar_estado_atencion(atencion.codigo, "No atendida")
                else:
                    self.actualizar_estado_cita(cita.codigo, "No atendida")
                cambios += 1

        return cambios
    def actualizar_estado_cita(
        self,
        codigo_cita,
        nuevo_estado
    ):

        if nuevo_estado not in Cita.ESTADOS_VALIDOS:
            raise ValueError(
                "Estado inválido. Use: "
                "Pendiente, En proceso, Atendida, Reprogramada, No atendida o Cancelada."
            )

        cita = next(
            (
                existente
                for existente in self._citas
                if existente.codigo
                == codigo_cita
            ),
            None
        )

        if cita is None:
            raise ValueError(
                "No se encontró la cita."
            )

        self._repositorio.actualizar_estado_cita(
            codigo_cita,
            nuevo_estado
        )

        cita.estado = nuevo_estado

