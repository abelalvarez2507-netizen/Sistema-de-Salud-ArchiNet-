import sqlite3



from servicios.persistencia.gestor_bd import GestorBaseDatos

from servicios.seguridad.seguridad import SeguridadDatos







class RepositorioPacientesMixin:
    """Operaciones de persistencia para pacientes."""

    def guardar_paciente(

        self,

        paciente

    ):



        try:



            with self._conexion:



                self._conexion.execute(

                    """

                    INSERT INTO pacientes

                    (

                        codigo,

                        dni_hash,

                        dni_salt,

                        nombre,

                        edad

                    )

                    VALUES (?, ?, ?, ?, ?)

                    """,

                    (

                        paciente.codigo,

                        paciente.dni_hash,

                        paciente.dni_salt,

                        paciente.nombre,

                        paciente.edad

                    )

                )



        except sqlite3.IntegrityError as error:



            raise ValueError(

                "No se pudo guardar el paciente. "

                "El código puede estar duplicado."

            ) from error

    def eliminar_paciente(self, codigo):

        """Deshace el alta de un paciente recién creado (sin citas)."""

        with self._conexion:

            self._conexion.execute(

                "DELETE FROM pacientes WHERE codigo = ?",

                (codigo,),

            )

    def obtener_pacientes(self):



        cursor = self._conexion.cursor()



        return cursor.execute(

            """

            SELECT

                codigo,

                dni_hash,

                dni_salt,

                nombre,

                edad

            FROM pacientes

            ORDER BY codigo

            """

        ).fetchall()

    def existe_dni_paciente(

        self,

        dni

    ):



        filas = self._conexion.execute(

            """

            SELECT

                dni_hash,

                dni_salt

            FROM pacientes

            WHERE dni_hash IS NOT NULL

              AND dni_salt IS NOT NULL

            """

        ).fetchall()



        return any(

            SeguridadDatos.verificar(

                dni,

                sal,

                resumen

            )

            for (

                resumen,

                sal

            ) in filas

        )


