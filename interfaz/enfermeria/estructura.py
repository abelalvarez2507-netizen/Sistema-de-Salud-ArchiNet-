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




class EnfermeriaEstructuraMixin:

    def _limpiar(self):
        for widget in self.ventana.winfo_children():
            try:
                widget.destroy()
            except tk.TclError:
                pass
    def _boton(self, padre, texto, comando, principal=False):
        return tk.Button(
            padre,
            text=texto,
            command=comando,
            font=FUENTE_BOTON,
            bg=COLOR_ROJO if principal else COLOR_PANEL_CLARO,
            fg=COLOR_BLANCO if principal else COLOR_TEXTO,
            activebackground=COLOR_ROJO_CLARO,
            activeforeground=COLOR_BLANCO,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=14,
            pady=8,
        )
    def _iniciar_pantalla(self, titulo, subtitulo="", mostrar_volver=False):
        self._limpiar()
        instalar_navegacion(
            self.ventana,
            volver=self.cerrar_sesion if not mostrar_volver else self.mostrar_inicio,
            inicio=self.cerrar_sesion,
        )
        vista = VistaDesplazable(self.ventana, COLOR_FONDO)
        vista.pack(fill="both", expand=True)
        contenido = vista.contenido
        contenido.configure(padx=24, pady=18)

        barra = tk.Frame(contenido, bg=COLOR_FONDO)
        barra.pack(fill="x", pady=(0, 12))
        if mostrar_volver:
            self._boton(barra, "←  Inicio de enfermería", self.mostrar_inicio).pack(
                side="left"
            )
        self._boton(barra, "Cerrar sesión", self.cerrar_sesion).pack(side="right")
        tk.Label(
            barra,
            text="ARCHINET",
            font=FUENTE_LOGO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(side="right", padx=(0, 18))
        tk.Frame(contenido, bg=COLOR_ROJO, height=3).pack(fill="x", pady=(0, 18))
        tk.Label(
            contenido,
            text=titulo,
            font=FUENTE_TITULO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            wraplength=900,
            justify="left",
        ).pack(anchor="w", pady=(0, 4))
        if subtitulo:
            tk.Label(
                contenido,
                text=subtitulo,
                font=FUENTE_SUBTITULO,
                fg=COLOR_GRIS_CLARO,
                bg=COLOR_FONDO,
                wraplength=900,
                justify="left",
            ).pack(anchor="w", pady=(0, 16))
        return contenido
    @staticmethod
    def _tarjeta(padre, titulo=None, fondo=COLOR_PANEL):
        tarjeta = tk.Frame(
            padre,
            bg=fondo,
            padx=16,
            pady=14,
            highlightthickness=1,
            highlightbackground="#DCE8E1",
        )
        if titulo:
            tk.Label(
                tarjeta,
                text=titulo,
                font=("Arial", 14, "bold"),
                fg=COLOR_TEXTO,
                bg=fondo,
            ).pack(anchor="w", pady=(0, 10))
        return tarjeta
    def _crear_estadisticas(self, padre, datos):
        zona = tk.Frame(padre, bg=COLOR_FONDO)
        zona.pack(fill="x", pady=(0, 16))
        for columna in range(len(datos)):
            zona.columnconfigure(columna, weight=1, uniform="estadisticas_enfermeria")
        for columna, (valor, etiqueta) in enumerate(datos):
            tarjeta = tk.Frame(
                zona,
                bg=COLOR_PANEL,
                padx=14,
                pady=13,
                highlightthickness=1,
                highlightbackground="#DCE8E1",
            )
            tarjeta.grid(row=0, column=columna, sticky="nsew", padx=5)
            tk.Label(
                tarjeta,
                text=str(valor),
                font=("Arial", 22, "bold"),
                fg=COLOR_ROJO,
                bg=COLOR_PANEL,
            ).pack(anchor="w")
            tk.Label(
                tarjeta,
                text=etiqueta,
                font=("Arial", 9),
                fg=COLOR_GRIS,
                bg=COLOR_PANEL,
                wraplength=190,
                justify="left",
            ).pack(anchor="w", pady=(4, 0))
    def _crear_modulo(self, padre, fila, columna, icono, titulo, descripcion, comando):
        tarjeta = tk.Frame(
            padre,
            bg=COLOR_PANEL,
            padx=16,
            pady=14,
            highlightthickness=1,
            highlightbackground="#DCE8E1",
        )
        tarjeta.grid(row=fila, column=columna, sticky="nsew", padx=6, pady=6)
        tarjeta.columnconfigure(0, weight=1)
        tk.Label(
            tarjeta,
            text=icono,
            font=("Arial", 21, "bold"),
            fg=COLOR_ROJO,
            bg=COLOR_PANEL,
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            tarjeta,
            text=titulo,
            font=("Arial", 13, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_PANEL,
            wraplength=350,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(4, 3))
        if descripcion:
            tk.Label(
                tarjeta,
                text=descripcion,
                font=("Arial", 9),
                fg=COLOR_GRIS,
                bg=COLOR_PANEL,
                wraplength=350,
                justify="left",
            ).grid(row=2, column=0, sticky="w", pady=(0, 12))
        self._boton(tarjeta, "Abrir", comando, principal=True).grid(
            row=3, column=0, sticky="ew"
        )
    def _etiqueta_campo(self, padre, texto, fila, columna):
        tk.Label(
            padre,
            text=texto,
            font=("Arial", 10, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_PANEL,
            anchor="w",
        ).grid(row=fila, column=columna, sticky="ew", padx=7, pady=(5, 2))
    def _poner_placeholder(self, campo, texto, solo_lectura=False):
        campo.placeholder_activo = True
        campo.placeholder_texto = texto
        campo.insert(0, texto)
        campo.configure(fg=COLOR_GRIS)
        if solo_lectura:
            return

        def quitar(_evento=None):
            if campo.placeholder_activo:
                campo.delete(0, tk.END)
                campo.configure(fg=COLOR_TEXTO)
                campo.placeholder_activo = False

        def restaurar(_evento=None):
            if not campo.get().strip():
                campo.insert(0, texto)
                campo.configure(fg=COLOR_GRIS)
                campo.placeholder_activo = True

        campo.bind("<FocusIn>", quitar, add="+")
        campo.bind("<FocusOut>", restaurar, add="+")
    def _valor_campo(self, campo):
        if getattr(campo, "placeholder_activo", False):
            return ""
        return campo.get().strip()
    def _entrada_campo(
        self,
        padre,
        campos,
        clave,
        texto,
        fila,
        columna,
        placeholder=None,
        solo_lectura=False,
    ):
        self._etiqueta_campo(padre, texto, fila, columna)
        entrada = tk.Entry(
            padre,
            font=("Arial", 11),
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            relief="flat",
            bd=0,
        )
        entrada.grid(row=fila + 1, column=columna, sticky="ew", padx=7, pady=(0, 7), ipady=7)
        if placeholder:
            self._poner_placeholder(entrada, placeholder, solo_lectura)
        if solo_lectura:
            entrada.configure(state="readonly")
        campos[clave] = entrada
        return entrada
    def _combo_campo(
        self,
        padre,
        campos,
        clave,
        texto,
        fila,
        columna,
        opciones,
        placeholder,
        al_seleccionar=None,
    ):
        self._etiqueta_campo(padre, texto, fila, columna)
        campo = ttk.Combobox(
            padre,
            values=(placeholder, *opciones),
            state="readonly",
            font=("Arial", 11),
        )
        campo.grid(
            row=fila + 1,
            column=columna,
            sticky="ew",
            padx=7,
            pady=(0, 7),
            ipady=5,
        )
        campo.set(placeholder)
        campo.placeholder_activo = True
        campo.configure(foreground=COLOR_GRIS)

        def seleccion(_evento=None):
            campo.placeholder_activo = campo.get() == placeholder
            campo.configure(
                foreground=COLOR_GRIS if campo.placeholder_activo else COLOR_TEXTO
            )
            if al_seleccionar:
                al_seleccionar(campo.get())

        campo.bind("<<ComboboxSelected>>", seleccion)
        campos[clave] = campo
        return campo
    def _configurar_fecha(self, campo, al_cambiar=None):
        configurar_mascara_fecha(campo, al_cambiar)
        if al_cambiar:
            campo.bind("<FocusOut>", lambda _evento: al_cambiar(), add="+")
    def _lista_medicamentos(self, padre, medicamentos):
        if not medicamentos:
            tk.Label(
                padre,
                text="No hay medicamentos disponibles para mostrar.",
                font=("Arial", 10),
                fg=COLOR_GRIS,
                bg=COLOR_PANEL,
            ).pack(anchor="w", pady=5)
            return

        cabecera = tk.Frame(padre, bg=COLOR_PANEL_CLARO, padx=8, pady=7)
        cabecera.pack(fill="x", pady=(0, 4))
        for columna, texto in enumerate(("Medicamento / presentación", "Lote / vencimiento", "Stock / precio")):
            cabecera.columnconfigure(columna, weight=(2 if columna == 0 else 1))
            tk.Label(
                cabecera,
                text=texto,
                font=("Arial", 9, "bold"),
                fg=COLOR_TEXTO,
                bg=COLOR_PANEL_CLARO,
                anchor="w",
            ).grid(row=0, column=columna, sticky="ew", padx=4)
        for medicamento in medicamentos:
            (
                codigo,
                nombre,
                principio_activo,
                presentacion,
                lote,
                vencimiento,
                stock,
                stock_minimo,
                precio,
                registrado_por,
                creado_en,
            ) = medicamento
            fila = tk.Frame(padre, bg=COLOR_PANEL, padx=8, pady=8)
            fila.pack(fill="x")
            for columna, peso in enumerate((2, 1, 1)):
                fila.columnconfigure(columna, weight=peso)
            nombre_detalle = nombre
            if presentacion:
                nombre_detalle += f" · {presentacion}"
            if principio_activo:
                nombre_detalle += f"\n{principio_activo}"
            detalles = (
                nombre_detalle,
                f"{lote}\nVence: {vencimiento}",
                f"{stock} un. · S/ {float(precio):.2f}\nMínimo: {stock_minimo}",
            )
            for columna, texto in enumerate(detalles):
                tk.Label(
                    fila,
                    text=texto,
                    font=("Arial", 9),
                    fg=COLOR_TEXTO,
                    bg=COLOR_PANEL,
                    anchor="w",
                    justify="left",
                    wraplength=260,
                ).grid(row=0, column=columna, sticky="ew", padx=4)
            tk.Frame(padre, bg=COLOR_PANEL_CLARO, height=1).pack(fill="x")

