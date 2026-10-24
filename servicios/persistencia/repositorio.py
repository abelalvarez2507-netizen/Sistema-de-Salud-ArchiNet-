import sqlite3



from servicios.persistencia.gestor_bd import GestorBaseDatos

from servicios.seguridad.seguridad import SeguridadDatos







from servicios.persistencia.pacientes import RepositorioPacientesMixin
from servicios.persistencia.personal import RepositorioPersonalMixin
from servicios.persistencia.cuentas import RepositorioCuentasMixin
from servicios.persistencia.citas import RepositorioCitasMixin
from servicios.persistencia.atenciones import RepositorioAtencionesMixin
from servicios.persistencia.medicamentos import RepositorioMedicamentosMixin
from servicios.persistencia.esquema import RepositorioEsquemaMixin

class RepositorioSalud(RepositorioEsquemaMixin, RepositorioPacientesMixin, RepositorioPersonalMixin, RepositorioCuentasMixin, RepositorioCitasMixin, RepositorioAtencionesMixin, RepositorioMedicamentosMixin):
    def __init__(

        self,

        ruta_bd="datos/salud.db"

    ):



        self._ruta_bd = ruta_bd



        self._gestor_bd = (

            GestorBaseDatos()

        )



        self._conexion = (

            self._gestor_bd.conectar(

                ruta_bd

            )

        )



        self._conexion.execute("PRAGMA foreign_keys = ON")

        self._crear_tablas()

        self._migrar_base_datos()

    def cerrar(self):



        self._gestor_bd.cerrar(

            self._ruta_bd

        )


