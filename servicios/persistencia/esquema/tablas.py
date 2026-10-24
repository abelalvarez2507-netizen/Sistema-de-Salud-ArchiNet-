import sqlite3



from servicios.persistencia.gestor_bd import GestorBaseDatos

from servicios.seguridad.seguridad import SeguridadDatos









class TablasRepositorioMixin:
    """Creación de tablas e índices del repositorio."""

    def _crear_tablas(self):



        cursor = self._conexion.cursor()



        cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS pacientes (

                codigo TEXT PRIMARY KEY,

                dni TEXT,

                dni_hash TEXT,

                dni_salt TEXT,

                nombre TEXT NOT NULL,

                edad INTEGER NOT NULL

            )

            """

        )



        cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS personal (

                codigo_profesional TEXT PRIMARY KEY,

                dni TEXT,

                dni_hash TEXT,

                dni_salt TEXT,

                nombre TEXT NOT NULL,

                edad INTEGER NOT NULL,

                especialidad TEXT NOT NULL

            )

            """

        )



        cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS citas (

                codigo TEXT PRIMARY KEY,

                paciente_codigo TEXT NOT NULL,

                profesional_codigo TEXT NOT NULL,

                fecha TEXT NOT NULL,

                hora TEXT NOT NULL DEFAULT '09:00',

                motivo TEXT NOT NULL,

                estado TEXT NOT NULL

            )

            """

        )



        cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS atenciones (
                codigo TEXT PRIMARY KEY,
                cita_codigo TEXT NOT NULL,
                diagnostico TEXT NOT NULL,
                estado TEXT NOT NULL,
                profesional_derivado_codigo TEXT,
                informe_derivacion TEXT NOT NULL DEFAULT ''
            )
            """

        )



        cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS recetas_medicas (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                atencion_codigo TEXT NOT NULL,

                medicamento TEXT NOT NULL,

                dias INTEGER NOT NULL CHECK (dias > 0),

                cada_cuanto TEXT NOT NULL,

                FOREIGN KEY (atencion_codigo) REFERENCES atenciones(codigo) ON DELETE CASCADE

            )

            """

        )



        cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS cuentas_acceso (

                usuario TEXT PRIMARY KEY COLLATE NOCASE,

                rol TEXT NOT NULL CHECK (

                    rol IN (

                        'paciente',

                        'administrativa',

                        'profesional',

                        'enfermeria'

                    )

                ),

                codigo_referencia TEXT,

                password_hash TEXT NOT NULL,

                password_salt TEXT NOT NULL,

                activo INTEGER NOT NULL DEFAULT 1,

                creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                UNIQUE (rol, codigo_referencia)

            )

            """

        )

        cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS medicamentos (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nombre TEXT NOT NULL,

                principio_activo TEXT NOT NULL DEFAULT '',

                presentacion TEXT NOT NULL DEFAULT '',

                lote TEXT NOT NULL,

                vencimiento TEXT NOT NULL,

                stock INTEGER NOT NULL CHECK (stock >= 0),

                stock_minimo INTEGER NOT NULL DEFAULT 0 CHECK (stock_minimo >= 0),

                precio_venta REAL NOT NULL CHECK (precio_venta >= 0),

                registrado_por TEXT NOT NULL,

                creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                UNIQUE (nombre COLLATE NOCASE, lote COLLATE NOCASE)

            )

            """

        )

        cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS ventas_medicamentos (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                medicamento_id INTEGER NOT NULL,

                medicamento_nombre TEXT NOT NULL,

                lote TEXT NOT NULL,

                cantidad INTEGER NOT NULL CHECK (cantidad > 0),

                precio_unitario REAL NOT NULL CHECK (precio_unitario >= 0),

                total REAL NOT NULL CHECK (total >= 0),

                cliente TEXT NOT NULL DEFAULT '',

                paciente_codigo TEXT NOT NULL,

                vendido_por TEXT NOT NULL,

                vendido_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id),

                FOREIGN KEY (paciente_codigo) REFERENCES pacientes(codigo)

            )

            """

        )

        cursor.execute(

            """

            CREATE UNIQUE INDEX IF NOT EXISTS una_cuenta_administrativa

            ON cuentas_acceso (rol)

            WHERE rol = 'administrativa'

            """

        )



        self._conexion.commit()

