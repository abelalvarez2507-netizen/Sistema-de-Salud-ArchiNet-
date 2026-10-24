import sqlite3



from servicios.persistencia.gestor_bd import GestorBaseDatos

from servicios.seguridad.seguridad import SeguridadDatos







class RepositorioCuentasMixin:
    """Operaciones de persistencia para cuentas."""

    def obtener_datos_paciente_acceso(self, codigo):

        """Devuelve solo los datos necesarios para comprobar la identidad."""

        return self._conexion.execute(

            """

            SELECT codigo, dni_hash, dni_salt

            FROM pacientes

            WHERE codigo = ? COLLATE NOCASE

            """,

            (codigo.strip(),),

        ).fetchone()

    def obtener_datos_personal_acceso(self, codigo):

        """Devuelve solo los datos necesarios para comprobar la identidad."""

        return self._conexion.execute(

            """

            SELECT codigo_profesional, dni_hash, dni_salt, especialidad

            FROM personal

            WHERE codigo_profesional = ? COLLATE NOCASE

            """,

            (codigo.strip(),),

        ).fetchone()

    def obtener_datos_personal_por_dni(self, dni):

        """Busca el registro de personal verificando el DNI protegido."""

        filas = self._conexion.execute(

            """

            SELECT codigo_profesional, dni_hash, dni_salt, especialidad

            FROM personal

            WHERE dni_hash IS NOT NULL AND dni_salt IS NOT NULL

            """

        ).fetchall()

        for codigo, resumen, sal, especialidad in filas:

            if SeguridadDatos.verificar(dni, sal, resumen):

                return codigo, resumen, sal, especialidad

        return None

    def obtener_cuenta_acceso(self, usuario):

        return self._conexion.execute(

            """

            SELECT usuario, rol, codigo_referencia, password_hash, password_salt, activo

            FROM cuentas_acceso

            WHERE usuario = ? COLLATE NOCASE

            """,

            (usuario.strip(),),

        ).fetchone()

    def contar_cuentas_acceso(self, rol):

        fila = self._conexion.execute(

            "SELECT COUNT(*) FROM cuentas_acceso WHERE rol = ?",

            (rol,),

        ).fetchone()

        return fila[0]

    def guardar_cuenta_acceso(

        self,

        usuario,

        rol,

        codigo_referencia,

        password_hash,

        password_salt,

        solo_primera_administrativa=False,

    ):

        """Guarda una cuenta y permite crear solo una cuenta administrativa inicial."""

        try:

            with self._conexion:

                if (

                    solo_primera_administrativa

                    and self.contar_cuentas_acceso("administrativa")

                ):

                    raise ValueError(

                        "Ya existe una cuenta administrativa configurada."

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

                        codigo_referencia,

                        password_hash,

                        password_salt,

                    ),

                )

        except sqlite3.IntegrityError as error:

            raise ValueError(

                "El usuario ya existe o ya tiene una cuenta para este rol."

            ) from error



    def eliminar_cuenta_acceso(self, usuario):
        with self._conexion:
            self._conexion.execute(
                "DELETE FROM cuentas_acceso WHERE usuario = ? COLLATE NOCASE",
                (usuario.strip(),),
            )
