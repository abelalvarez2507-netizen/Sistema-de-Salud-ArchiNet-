import sqlite3



from servicios.persistencia.gestor_bd import GestorBaseDatos

from servicios.seguridad.seguridad import SeguridadDatos







class RepositorioPersonalMixin:
    """Operaciones de persistencia para personal."""

    def guardar_personal(

        self,

        profesional

    ):



        try:



            with self._conexion:



                self._conexion.execute(

                    """

                    INSERT INTO personal

                    (

                        codigo_profesional,

                        dni_hash,

                        dni_salt,

                        nombre,

                        edad,

                        especialidad

                    )

                    VALUES (?, ?, ?, ?, ?, ?)

                    """,

                    (

                        profesional.codigo_profesional,

                        profesional.dni_hash,

                        profesional.dni_salt,

                        profesional.nombre,

                        profesional.edad,

                        profesional.especialidad

                    )

                )



        except sqlite3.IntegrityError as error:



            raise ValueError(

                "No se pudo guardar el profesional. "

                "El código puede estar duplicado."

            ) from error

    def guardar_personal_con_cuenta(

        self,

        profesional,

        usuario,

        rol,

        password_hash,

        password_salt,

    ):

        """Guarda el registro nuevo y su cuenta dentro de una sola transacción."""

        try:

            with self._conexion:

                self._conexion.execute(

                    """

                    INSERT INTO personal

                    (

                        codigo_profesional,

                        dni_hash,

                        dni_salt,

                        nombre,

                        edad,

                        especialidad

                    )

                    VALUES (?, ?, ?, ?, ?, ?)

                    """,

                    (

                        profesional.codigo_profesional,

                        profesional.dni_hash,

                        profesional.dni_salt,

                        profesional.nombre,

                        profesional.edad,

                        profesional.especialidad,

                    ),

                )

                self._conexion.execute(

                    """

                    INSERT INTO cuentas_acceso

                    (usuario, rol, codigo_referencia, password_hash, password_salt)

                    VALUES (?, ?, ?, ?, ?)

                    """,

                    (

                        usuario,

                        rol,

                        profesional.codigo_profesional,

                        password_hash,

                        password_salt,

                    ),

                )

        except sqlite3.IntegrityError as error:

            raise ValueError(

                "No se pudo crear la cuenta. El usuario, el DNI o el código "

                "ya están registrados."

            ) from error

    def obtener_personal(self):



        cursor = self._conexion.cursor()



        return cursor.execute(

            """

            SELECT

                codigo_profesional,

                dni_hash,

                dni_salt,

                nombre,

                edad,

                especialidad

            FROM personal

            ORDER BY codigo_profesional

            """

        ).fetchall()

    def existe_dni_personal(

        self,

        dni

    ):



        filas = self._conexion.execute(

            """

            SELECT

                dni_hash,

                dni_salt

            FROM personal

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


