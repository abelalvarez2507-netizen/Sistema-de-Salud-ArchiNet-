import sqlite3



from servicios.persistencia.gestor_bd import GestorBaseDatos

from servicios.seguridad.seguridad import SeguridadDatos









class MigracionesRepositorioMixin:
    """Migración del esquema y conservación de datos existentes."""

    def _migrar_base_datos(self):



        cursor = self._conexion.cursor()



        # -----------------------------------------------------

        # PACIENTES

        # -----------------------------------------------------



        columnas_pacientes = [

            fila[1]

            for fila in cursor.execute(

                "PRAGMA table_info(pacientes)"

            ).fetchall()

        ]



        if "dni" not in columnas_pacientes:



            cursor.execute(

                """

                ALTER TABLE pacientes

                ADD COLUMN dni TEXT

                """

            )



        if "dni_hash" not in columnas_pacientes:



            cursor.execute(

                """

                ALTER TABLE pacientes

                ADD COLUMN dni_hash TEXT

                """

            )



        if "dni_salt" not in columnas_pacientes:



            cursor.execute(

                """

                ALTER TABLE pacientes

                ADD COLUMN dni_salt TEXT

                """

            )



        # -----------------------------------------------------

        # PERSONAL

        # -----------------------------------------------------



        columnas_personal = [

            fila[1]

            for fila in cursor.execute(

                "PRAGMA table_info(personal)"

            ).fetchall()

        ]



        if "dni" not in columnas_personal:



            cursor.execute(

                """

                ALTER TABLE personal

                ADD COLUMN dni TEXT

                """

            )



        if "dni_hash" not in columnas_personal:



            cursor.execute(

                """

                ALTER TABLE personal

                ADD COLUMN dni_hash TEXT

                """

            )



        if "dni_salt" not in columnas_personal:



            cursor.execute(

                """

                ALTER TABLE personal

                ADD COLUMN dni_salt TEXT

                """

            )



        columnas_ventas = [

            fila[1]

            for fila in cursor.execute(

                "PRAGMA table_info(ventas_medicamentos)"

            ).fetchall()

        ]

        if "paciente_codigo" not in columnas_ventas:

            cursor.execute(

                "ALTER TABLE ventas_medicamentos ADD COLUMN paciente_codigo TEXT"

            )

        # Preserve older rows when the former free-text client field already

        # contains an exact patient code; names are never guessed or matched.

        cursor.execute(

            """

            UPDATE ventas_medicamentos

            SET paciente_codigo = (

                SELECT codigo FROM pacientes

                WHERE codigo = ventas_medicamentos.cliente COLLATE NOCASE

            )

            WHERE paciente_codigo IS NULL

              AND EXISTS (

                SELECT 1 FROM pacientes

                WHERE codigo = ventas_medicamentos.cliente COLLATE NOCASE

              )

            """

        )



        columnas_citas = [

            fila[1]

            for fila in cursor.execute(

                "PRAGMA table_info(citas)"

            ).fetchall()

        ]



        if "hora" not in columnas_citas:
            cursor.execute(
                "ALTER TABLE citas ADD COLUMN hora TEXT NOT NULL DEFAULT '09:00'"
            )

        columnas_atenciones = [
            fila[1]
            for fila in cursor.execute(
                "PRAGMA table_info(atenciones)"
            ).fetchall()
        ]
        if "profesional_derivado_codigo" not in columnas_atenciones:
            cursor.execute(
                "ALTER TABLE atenciones ADD COLUMN profesional_derivado_codigo TEXT"
            )

        if "informe_derivacion" not in columnas_atenciones:
            cursor.execute(
                "ALTER TABLE atenciones ADD COLUMN informe_derivacion TEXT NOT NULL DEFAULT ''"
            )
        cursor.execute(
            """
            UPDATE atenciones
            SET informe_derivacion = diagnostico
            WHERE profesional_derivado_codigo IS NOT NULL
              AND informe_derivacion = ''
            """
        )


        # -----------------------------------------------------

        # MIGRACIÓN DE DNI DE PACIENTES

        # -----------------------------------------------------



        pacientes = cursor.execute(

            """

            SELECT

                codigo,

                dni

            FROM pacientes

            WHERE dni IS NOT NULL

              AND dni != ''

              AND (

                    dni_hash IS NULL

                    OR dni_salt IS NULL

                  )

            """

        ).fetchall()



        for codigo, dni in pacientes:



            sal, resumen = (

                SeguridadDatos.proteger(

                    str(dni)

                )

            )



            cursor.execute(

                """

                UPDATE pacientes

                SET

                    dni = NULL,

                    dni_hash = ?,

                    dni_salt = ?

                WHERE codigo = ?

                """,

                (

                    resumen,

                    sal,

                    codigo

                )

            )



        # Limpiar cualquier copia antigua del DNI en texto plano cuando

        # ya existe una huella protegida. La columna histórica se mantiene

        # únicamente por compatibilidad con bases de datos anteriores.

        cursor.execute(

            """

            UPDATE pacientes

            SET dni = NULL

            WHERE dni_hash IS NOT NULL

              AND dni_salt IS NOT NULL

              AND dni IS NOT NULL

            """

        )



        # -----------------------------------------------------

        # MIGRACIÓN DE DNI DE PERSONAL

        # -----------------------------------------------------



        profesionales = cursor.execute(

            """

            SELECT

                codigo_profesional,

                dni

            FROM personal

            WHERE dni IS NOT NULL

              AND dni != ''

              AND (

                    dni_hash IS NULL

                    OR dni_salt IS NULL

                  )

            """

        ).fetchall()



        for codigo, dni in profesionales:



            sal, resumen = (

                SeguridadDatos.proteger(

                    str(dni)

                )

            )



            cursor.execute(

                """

                UPDATE personal

                SET

                    dni = NULL,

                    dni_hash = ?,

                    dni_salt = ?

                WHERE codigo_profesional = ?

                """,

                (

                    resumen,

                    sal,

                    codigo

                )

            )



        cursor.execute(

            """

            UPDATE personal

            SET dni = NULL

            WHERE dni_hash IS NOT NULL

              AND dni_salt IS NOT NULL

              AND dni IS NOT NULL

            """

        )



        # -----------------------------------------------------

        # ESTADOS

        # -----------------------------------------------------



        cursor.execute(

            """

            UPDATE citas

            SET estado = 'Reprogramada'

            WHERE estado IN ('Reprogramar', 'Reprogramada')

            """

        )



        self._conexion.commit()

