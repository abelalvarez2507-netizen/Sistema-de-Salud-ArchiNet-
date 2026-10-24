"""Portal de enfermería con agenda, inventario y ventas de medicamentos."""

from datetime import date, datetime
import tkinter as tk
from tkinter import ttk

from interfaz.estilos import (
    COLOR_BLANCO,
    COLOR_FONDO,
    COLOR_GRIS,
    COLOR_GRIS_CLARO,
    COLOR_PANEL,
    COLOR_PANEL_CLARO,
    COLOR_ROJO,
    COLOR_ROJO_CLARO,
    COLOR_TEXTO,
    FUENTE_BOTON,
    FUENTE_LOGO,
    FUENTE_SUBTITULO,
    FUENTE_TITULO,
)
from interfaz.navegacion import VistaDesplazable, instalar_navegacion
from interfaz.campos import configurar_mascara_fecha
from servicios.seguridad.autenticacion import ServicioAutenticacion
from servicios.gestion.sistema_salud import SistemaSalud


PRODUCTOS_MEDICAMENTO = {
    "Paracetamol": "Paracetamol",
    "Ibuprofeno": "Ibuprofeno",
    "Amoxicilina": "Amoxicilina",
    "Loratadina": "Loratadina",
}

PRINCIPIOS_ACTIVOS = (
    "Paracetamol",
    "Ibuprofeno",
    "Amoxicilina",
    "Loratadina",
    "Ácido acetilsalicílico",
    "Diclofenaco",
    "Naproxeno",
    "Ketorolaco",
    "Amoxicilina + ácido clavulánico",
    "Ampicilina",
    "Azitromicina",
    "Claritromicina",
    "Cefalexina",
    "Ceftriaxona",
    "Ciprofloxacino",
    "Doxiciclina",
    "Eritromicina",
    "Metronidazol",
    "Nitrofurantoína",
    "Sulfametoxazol + trimetoprima",
    "Clindamicina",
    "Cetirizina",
    "Clorfenamina",
    "Omeprazol",
    "Pantoprazol",
    "Metoclopramida",
    "Ondansetrón",
    "Loperamida",
    "Metformina",
    "Glibenclamida",
    "Insulina humana",
    "Enalapril",
    "Losartán",
    "Amlodipino",
    "Hidroclorotiazida",
    "Furosemida",
    "Atorvastatina",
    "Levotiroxina",
    "Salbutamol",
    "Prednisona",
)




class EnfermeriaMedicamentosMixin:

    def mostrar_registro_medicamentos(self, mensaje=""):
        contenido = self._iniciar_pantalla(
            "Registrar medicamentos",
            "",
            mostrar_volver=True,
        )
        panel = self._tarjeta(contenido, "Datos del medicamento")
        panel.pack(fill="x", pady=(0, 12))
        formulario = tk.Frame(panel, bg=COLOR_PANEL)
        formulario.pack(fill="x")
        formulario.columnconfigure(0, weight=1, uniform="campos_medicamento")
        formulario.columnconfigure(1, weight=1, uniform="campos_medicamento")
        campos = {}
        nombre = self._combo_campo(
            formulario,
            campos,
            "nombre",
            "Nombre del medicamento *",
            0,
            0,
            tuple(PRODUCTOS_MEDICAMENTO),
            "Selecciona medicamento",
        )
        principio = self._combo_campo(
            formulario,
            campos,
            "principio_activo",
            "Principio activo *",
            0,
            1,
            PRINCIPIOS_ACTIVOS,
            "Selecciona el principio activo",
        )

        def completar_principio(medicamento):
            activo = PRODUCTOS_MEDICAMENTO.get(medicamento)
            if activo:
                principio.set(activo)
                principio.placeholder_activo = False
                principio.configure(foreground=COLOR_TEXTO)

        nombre.bind("<<ComboboxSelected>>", lambda _evento: completar_principio(nombre.get()), add="+")
        self._entrada_campo(
            formulario,
            campos,
            "presentacion",
            "Presentación *",
            2,
            0,
            placeholder="Ej.: tableta de 500 mg",
        )
        lote = self._entrada_campo(
            formulario,
            campos,
            "lote",
            "Número de lote *",
            2,
            1,
            placeholder="Ej.: L-2026-001",
        )
        vencimiento = self._entrada_campo(
            formulario,
            campos,
            "vencimiento",
            "Vencimiento (DD/MM/AAAA) *",
            4,
            0,
            placeholder="Ej.: 25/07/2027",
        )
        self._entrada_campo(
            formulario, campos, "stock", "Stock inicial *", 4, 1,
            placeholder="Ej.: 100",
        )
        self._entrada_campo(
            formulario, campos, "stock_minimo", "Stock mínimo", 6, 0,
            placeholder="Ej.: 10",
        )
        self._entrada_campo(
            formulario, campos, "precio_venta", "Precio por unidad (S/) *", 6, 1,
            placeholder="Ej.: 1.50",
        )
        estado = tk.Label(
            panel,
            text=mensaje,
            font=("Arial", 9),
            fg=COLOR_ROJO if mensaje and not mensaje.startswith("Registrado") else COLOR_GRIS,
            bg=COLOR_PANEL,
            wraplength=850,
            justify="left",
        )
        estado.pack(fill="x", pady=(2, 8))

        def validar_vencimiento():
            valor = self._valor_campo(vencimiento)
            if not valor:
                return
            try:
                fecha = datetime.strptime(valor, "%d/%m/%Y").date()
            except ValueError:
                return
            if fecha < date.today():
                estado.configure(
                    text="La fecha de vencimiento no puede ser anterior a hoy.",
                    fg=COLOR_ROJO,
                )
            elif estado.cget("text") == "La fecha de vencimiento no puede ser anterior a hoy.":
                estado.configure(text="", fg=COLOR_GRIS)

        self._configurar_fecha(vencimiento, validar_vencimiento)

        def guardar():
            try:
                self.sistema.registrar_medicamento(
                    self._valor_campo(campos["nombre"]),
                    self._valor_campo(campos["principio_activo"]),
                    self._valor_campo(campos["presentacion"]),
                    self._valor_campo(campos["lote"]),
                    self._valor_campo(campos["vencimiento"]),
                    self._valor_campo(campos["stock"]),
                    self._valor_campo(campos["stock_minimo"]) or "0",
                    self._valor_campo(campos["precio_venta"]),
                    self.enfermero_actual.nombre,
                )
            except Exception as error:
                estado.configure(text=str(error), fg=COLOR_ROJO)
                return
            self.mostrar_registro_medicamentos(
                "Registrado."
            )

        self._boton(panel, "Guardar medicamento", guardar, principal=True).pack(
            fill="x", pady=(0, 4)
        )

        inventario = self._tarjeta(contenido, "Consulta de medicamentos disponibles")
        inventario.pack(fill="x", pady=(0, 12))
        disponibles = self.sistema.obtener_medicamentos_disponibles()
        self._lista_medicamentos(inventario, disponibles[:8])
        self._boton(
            inventario,
            "Ver inventario disponible",
            self.mostrar_medicamentos_disponibles,
        ).pack(anchor="e", pady=(10, 0))
    def mostrar_medicamentos_disponibles(self):
        contenido = self._iniciar_pantalla(
            "Medicamentos disponibles",
            "Solo se muestran lotes vigentes que tienen existencias.",
            mostrar_volver=True,
        )
        panel = self._tarjeta(contenido, "Buscar en inventario")
        panel.pack(fill="x")
        busqueda = tk.StringVar(master=self.ventana)
        campo = tk.Entry(
            panel,
            textvariable=busqueda,
            font=("Arial", 11),
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="flat",
            bd=0,
        )
        campo.pack(fill="x", ipady=7, pady=(0, 10))
        listado = tk.Frame(panel, bg=COLOR_PANEL)
        listado.pack(fill="x")

        def actualizar(*_args):
            for widget in listado.winfo_children():
                widget.destroy()
            filtro = busqueda.get().strip().casefold()
            disponibles = self.sistema.obtener_medicamentos_disponibles()
            resultados = [
                med
                for med in disponibles
                if not filtro or filtro in " ".join(map(str, (med[1], med[2], med[3], med[4]))).casefold()
            ]
            self._lista_medicamentos(listado, resultados)

        busqueda.trace_add("write", actualizar)
        actualizar()
    def mostrar_ventas(self, mensaje=""):
        contenido = self._iniciar_pantalla(
            "Registrar venta de medicamentos",
            "",
            mostrar_volver=True,
        )
        panel = self._tarjeta(contenido, "Nueva venta")
        panel.pack(fill="x", pady=(0, 12))
        panel.columnconfigure(0, weight=1)
        medicamentos = self.sistema.obtener_medicamentos_disponibles()
        opciones = {
            f"{med[1]} · Lote {med[4]} · {med[6]} un. · S/ {float(med[8]):.2f}": med
            for med in medicamentos
        }
        seleccion = tk.StringVar(master=self.ventana)
        combo = ttk.Combobox(
            panel,
            textvariable=seleccion,
            values=list(opciones),
            state="readonly" if opciones else "disabled",
            font=("Arial", 11),
        )
        combo.pack(fill="x", pady=(0, 8), ipady=4)
        if opciones:
            combo.current(0)
        else:
            seleccion.set("No hay medicamentos vigentes con stock disponible")

        tk.Label(
            panel,
            text="Cantidad",
            font=("Arial", 10, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_PANEL,
        ).pack(anchor="w", pady=(3, 2))
        cantidad = tk.Entry(
            panel,
            font=("Arial", 11),
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="flat",
            bd=0,
        )
        cantidad.pack(fill="x", ipady=7, pady=(0, 8))
        cantidad.insert(0, "1")
        tk.Label(
            panel,
            text="Código del paciente *",
            font=("Arial", 10, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_PANEL,
        ).pack(anchor="w", pady=(3, 2))
        codigo_paciente = tk.Entry(
            panel,
            font=("Arial", 11),
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="flat",
            bd=0,
        )
        codigo_paciente.pack(fill="x", ipady=7, pady=(0, 4))
        tk.Label(
            panel,
            text="La fecha y hora se guardan automáticamente al registrar.",
            font=("Arial", 9),
            fg=COLOR_GRIS,
            bg=COLOR_PANEL,
        ).pack(anchor="w", pady=(0, 8))
        estado = tk.Label(
            panel,
            text=mensaje,
            font=("Arial", 9),
            fg=COLOR_GRIS,
            bg=COLOR_PANEL,
            wraplength=850,
            justify="left",
        )
        estado.pack(anchor="w", pady=(0, 8))

        def guardar_venta():
            elegido = opciones.get(seleccion.get())
            if not elegido:
                estado.configure(text="Registra o selecciona un medicamento disponible.", fg=COLOR_ROJO)
                return
            try:
                _id, total, existencia = self.sistema.vender_medicamento(
                    elegido[0],
                    cantidad.get(),
                    codigo_paciente.get(),
                    self.enfermero_actual.nombre,
                )
            except Exception as error:
                estado.configure(text=str(error), fg=COLOR_ROJO)
                return
            self.mostrar_ventas(
                f"Venta registrada: S/ {total:.2f}. Existencia restante: {existencia} unidad(es)."
            )

        self._boton(panel, "Registrar venta", guardar_venta, principal=True).pack(
            fill="x"
        )

        inventario = self._tarjeta(contenido, "Medicamentos que puedes vender")
        inventario.pack(fill="x", pady=(0, 12))
        self._lista_medicamentos(inventario, medicamentos)

        historial = self._tarjeta(contenido, "Ventas recientes")
        historial.pack(fill="x", pady=(0, 12))
        ventas = self.sistema.obtener_ventas_medicamentos(50)
        if not ventas:
            tk.Label(
                historial,
                text="Todavía no hay ventas registradas.",
                font=("Arial", 10),
                fg=COLOR_GRIS,
                bg=COLOR_PANEL,
            ).pack(anchor="w")
        else:
            for venta in ventas:
                (_id, nombre, lote, unidades, precio, total, comprador, vendedor, fecha_hora, codigo_paciente) = venta
                detalle = (
                    f"{fecha_hora} · {nombre} · Lote {lote} · "
                    f"{unidades} un. · S/ {float(total):.2f}"
                )
                detalle += f" · Paciente {codigo_paciente or 'sin vincular'}"
                tk.Label(
                    historial,
                    text=detalle,
                    font=("Arial", 9),
                    fg=COLOR_TEXTO,
                    bg=COLOR_PANEL,
                    anchor="w",
                    justify="left",
                    wraplength=850,
                ).pack(fill="x", pady=4)
                tk.Frame(historial, bg=COLOR_PANEL_CLARO, height=1).pack(fill="x")

