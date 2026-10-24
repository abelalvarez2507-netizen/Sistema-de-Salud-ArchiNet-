import sqlite3



from servicios.persistencia.gestor_bd import GestorBaseDatos

from servicios.seguridad.seguridad import SeguridadDatos







class RepositorioAtencionesMixin:
    """Operaciones de persistencia para atenciones."""

    def guardar_atencion(

        self,

        atencion

    ):



        try:



            with self._conexion:



                self._conexion.execute(

                    """

                    INSERT INTO atenciones

                    (

                        codigo,

                        cita_codigo,
                        diagnostico,
                        estado,
                        profesional_derivado_codigo,
                        informe_derivacion
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,

                    (

                        atencion.codigo,

                        atencion.cita.codigo,
                        atencion.diagnostico,
                        atencion.estado,
                        (
                            atencion.profesional_derivado.codigo_profesional
                            if atencion.profesional_derivado
                            else None
                        ),
                        atencion.informe_derivacion,
                    )

                )

                self._guardar_recetas_en_transaccion(atencion.codigo, atencion.recetas)



        except sqlite3.IntegrityError as error:



            raise ValueError(

                "No se pudo guardar la atención."

            ) from error

    def _guardar_recetas_en_transaccion(self, codigo_atencion, recetas):

        self._conexion.execute(

            "DELETE FROM recetas_medicas WHERE atencion_codigo = ?",

            (codigo_atencion,),

        )

        self._conexion.executemany(

            """

            INSERT INTO recetas_medicas (atencion_codigo, medicamento, dias, cada_cuanto)

            VALUES (?, ?, ?, ?)

            """,

            [

                (codigo_atencion, receta.medicamento, receta.dias, receta.cada_cuanto)

                for receta in recetas

            ],

        )

    def guardar_recetas_atencion(self, codigo_atencion, recetas):

        try:

            with self._conexion:

                existe = self._conexion.execute(

                    "SELECT 1 FROM atenciones WHERE codigo = ?",

                    (codigo_atencion,),

                ).fetchone()

                if existe is None:

                    raise ValueError("No se encontró la atención para guardar sus recetas.")

                self._guardar_recetas_en_transaccion(codigo_atencion, recetas)

        except sqlite3.IntegrityError as error:

            raise ValueError("No se pudieron guardar las recetas médicas.") from error

    def obtener_recetas_atencion(self, codigo_atencion):

        return self._conexion.execute(

            """

            SELECT medicamento, dias, cada_cuanto

            FROM recetas_medicas

            WHERE atencion_codigo = ?

            ORDER BY id

            """,

            (codigo_atencion,),

        ).fetchall()

    def obtener_atenciones(self):



        cursor = self._conexion.cursor()



        return cursor.execute(

            """

            SELECT

                codigo,

                cita_codigo,

                diagnostico,
                estado,
                profesional_derivado_codigo,
                informe_derivacion
            FROM atenciones

            ORDER BY codigo

            """

        ).fetchall()

    def actualizar_estado_atencion(

        self,

        codigo_atencion,

        nuevo_estado

    ):



        with self._conexion:



            self._conexion.execute(

                """

                UPDATE atenciones

                SET estado = ?

                WHERE codigo = ?

                """,

                (

                    nuevo_estado,

                    codigo_atencion

                )

            )

    def actualizar_diagnostico_atencion(
        self,
        codigo_atencion,
        diagnostico,
        profesional_derivado_codigo=None,
        informe_derivacion=None,
    ):
        with self._conexion:
            self._conexion.execute(
                """
                UPDATE atenciones
                SET diagnostico = ?, profesional_derivado_codigo = ?,
                    informe_derivacion = COALESCE(?, informe_derivacion)
                WHERE codigo = ?
                """,
                (
                    diagnostico,
                    profesional_derivado_codigo,
                    informe_derivacion,
                    codigo_atencion,
                ),
            )

