import sqlite3



from servicios.persistencia.gestor_bd import GestorBaseDatos

from servicios.seguridad.seguridad import SeguridadDatos







class RepositorioMedicamentosMixin:
    """Operaciones de persistencia para medicamentos."""

    def guardar_medicamento(

        self,

        nombre,

        principio_activo,

        presentacion,

        lote,

        vencimiento,

        stock,

        stock_minimo,

        precio_venta,

        registrado_por,

    ):

        try:

            with self._conexion:

                cursor = self._conexion.execute(

                    """

                    INSERT INTO medicamentos (

                        nombre, principio_activo, presentacion, lote,

                        vencimiento, stock, stock_minimo, precio_venta,

                        registrado_por

                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

                    """,

                    (

                        nombre,

                        principio_activo,

                        presentacion,

                        lote,

                        vencimiento,

                        stock,

                        stock_minimo,

                        precio_venta,

                        registrado_por,

                    ),

                )

                return cursor.lastrowid

        except sqlite3.IntegrityError as error:

            raise ValueError(

                "Ya existe un registro con ese medicamento y lote."

            ) from error

    def obtener_medicamentos(self):

        return self._conexion.execute(

            """

            SELECT id, nombre, principio_activo, presentacion, lote,

                   vencimiento, stock, stock_minimo, precio_venta,

                   registrado_por, creado_en

            FROM medicamentos

            ORDER BY nombre COLLATE NOCASE, vencimiento, lote

            """

        ).fetchall()

    def obtener_medicamentos_disponibles(self, fecha_actual):

        return self._conexion.execute(

            """

            SELECT id, nombre, principio_activo, presentacion, lote,

                   vencimiento, stock, stock_minimo, precio_venta,

                   registrado_por, creado_en

            FROM medicamentos

            WHERE stock > 0 AND vencimiento >= ?

            ORDER BY nombre COLLATE NOCASE, vencimiento, lote

            """,

            (fecha_actual,),

        ).fetchall()

    def registrar_venta_medicamento(

        self,

        medicamento_id,

        cantidad,

        paciente_codigo,

        vendido_por,

        fecha_hora,

    ):

        try:

            with self._conexion:

                medicamento = self._conexion.execute(

                    """

                    SELECT nombre, lote, vencimiento, stock, precio_venta

                    FROM medicamentos WHERE id = ?

                    """,

                    (medicamento_id,),

                ).fetchone()

                if medicamento is None:

                    raise ValueError("El medicamento seleccionado ya no existe.")

                nombre, lote, vencimiento, stock, precio = medicamento

                if vencimiento < fecha_hora[:10]:

                    raise ValueError("No se puede vender un medicamento vencido.")

                if cantidad > stock:

                    raise ValueError(

                        f"Stock insuficiente. Solo quedan {stock} unidad(es)."

                    )

                total = round(float(precio) * cantidad, 2)

                actualizacion = self._conexion.execute(

                    """

                    UPDATE medicamentos

                    SET stock = stock - ?

                    WHERE id = ? AND stock >= ? AND vencimiento >= ?

                    """,

                    (cantidad, medicamento_id, cantidad, fecha_hora[:10]),

                )

                if actualizacion.rowcount != 1:

                    stock_actual = self._conexion.execute(

                        "SELECT stock FROM medicamentos WHERE id = ?",

                        (medicamento_id,),

                    ).fetchone()

                    if stock_actual is None:

                        raise ValueError("El medicamento seleccionado ya no existe.")

                    raise ValueError(

                        f"Stock insuficiente. Solo quedan {stock_actual[0]} unidad(es)."

                    )

                cursor = self._conexion.execute(

                    """

                    INSERT INTO ventas_medicamentos (

                        medicamento_id, medicamento_nombre, lote, cantidad,

                        precio_unitario, total, cliente, paciente_codigo,

                        vendido_por, vendido_en

                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

                    """,

                    (

                        medicamento_id,

                        nombre,

                        lote,

                        cantidad,

                        precio,

                        total,

                        paciente_codigo,

                        paciente_codigo,

                        vendido_por,

                        fecha_hora,

                    ),

                )

                return cursor.lastrowid, total, stock - cantidad

        except sqlite3.IntegrityError as error:

            raise ValueError("No se pudo guardar la venta.") from error

    def obtener_ventas_medicamentos(self, limite=100):

        return self._conexion.execute(

            """

            SELECT id, medicamento_nombre, lote, cantidad, precio_unitario,

                   total, cliente, vendido_por, vendido_en, paciente_codigo

            FROM ventas_medicamentos

            ORDER BY datetime(vendido_en) DESC, id DESC

            LIMIT ?

            """,

            (int(limite),),

        ).fetchall()

    def obtener_ventas_paciente(self, codigo_paciente):

        return self._conexion.execute(

            """

            SELECT id, medicamento_nombre, lote, cantidad, precio_unitario,

                   total, paciente_codigo, vendido_por, vendido_en

            FROM ventas_medicamentos

            WHERE paciente_codigo = ? COLLATE NOCASE

            ORDER BY datetime(vendido_en) DESC, id DESC

            """,

            (codigo_paciente,),

        ).fetchall()

    def obtener_estadisticas_medicamentos(self, fecha_actual):

        disponibles = self._conexion.execute(

            """

            SELECT COUNT(*), COALESCE(SUM(stock), 0)

            FROM medicamentos

            WHERE stock > 0 AND vencimiento >= ?

            """,

            (fecha_actual,),

        ).fetchone()

        ventas = self._conexion.execute(

            """

            SELECT COUNT(*), COALESCE(SUM(total), 0)

            FROM ventas_medicamentos

            WHERE substr(vendido_en, 1, 10) = ?

            """,

            (fecha_actual,),

        ).fetchone()

        return {

            "lotes_disponibles": disponibles[0],

            "unidades_disponibles": disponibles[1],

            "ventas_hoy": ventas[0],

            "monto_ventas_hoy": ventas[1],

        }


