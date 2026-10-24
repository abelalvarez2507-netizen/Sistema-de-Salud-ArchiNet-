import sqlite3



from servicios.persistencia.gestor_bd import GestorBaseDatos

from servicios.seguridad.seguridad import SeguridadDatos







class RepositorioCitasMixin:
    """Operaciones de persistencia para citas."""

    def guardar_cita(

        self,

        cita

    ):



        try:



            with self._conexion:



                self._conexion.execute(

                    """

                    INSERT INTO citas

                    (

                        codigo,

                        paciente_codigo,

                        profesional_codigo,

                        fecha,

                        hora,

                        motivo,

                        estado

                    )

                    VALUES (?, ?, ?, ?, ?, ?, ?)

                    """,

                    (

                        cita.codigo,

                        cita.paciente.codigo,

                        cita.profesional.codigo_profesional,

                        cita.fecha,

                        cita.hora,

                        cita.motivo,

                        cita.estado

                    )

                )



        except sqlite3.IntegrityError as error:



            raise ValueError(

                "No se pudo guardar la cita."

            ) from error

    def obtener_citas(self):



        cursor = self._conexion.cursor()



        return cursor.execute(

            """

            SELECT

                codigo,

                paciente_codigo,

                profesional_codigo,

                fecha,

                hora,

                motivo,

                estado

            FROM citas

            ORDER BY codigo

            """

        ).fetchall()

    def actualizar_estado_cita(

        self,

        codigo_cita,

        nuevo_estado

    ):



        with self._conexion:



            self._conexion.execute(

                """

                UPDATE citas

                SET estado = ?

                WHERE codigo = ?

                """,

                (

                    nuevo_estado,

                    codigo_cita

                )

            )

    def actualizar_agenda_cita(

        self,

        codigo_cita,

        fecha,

        hora,

        estado,

    ):

        with self._conexion:

            self._conexion.execute(

                "UPDATE citas SET fecha = ?, hora = ?, estado = ? WHERE codigo = ?",

                (fecha, hora, estado, codigo_cita),

            )


