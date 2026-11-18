# Archinet

## Sistema de gestión para un establecimiento de salud rural

Archinet es un prototipo académico de escritorio desarrollado
en Python para gestionar pacientes, profesionales de salud, citas, atenciones
médicas e informes básicos en un establecimiento de salud rural. Utiliza
Tkinter para la interfaz gráfica y SQLite para guardar la información.

## 1. Funcionalidades

- Registro, consulta y búsqueda de pacientes, profesionales y personal de enfermería.
- Códigos secuenciales independientes para profesionales (CMP001...), ventas/enfermería (MTF001...) y triaje (FAM001...), sin tope de numeración. El código médico secreto se solicita al crear la cuenta de acceso del personal.
- Al elegir Enfermería en la pantalla inicial, se puede ingresar al área de ventas o al área de triaje.
- Acceso a los módulos de paciente, profesional, ventas, triaje y administración.
- Inicio de sesión con cuentas independientes por rol. Los accesos no se
  conceden solo por conocer un código o un DNI.
- Las cuentas de personal se vinculan por DNI al registro administrativo o crean
  un registro nuevo con código automático y código médico autorizado, sin límite
  de numeración. Las cuentas de paciente existentes se verifican con código y DNI.
- Autorregistro de pacientes nuevos desde el acceso de Paciente: la persona
  indica nombre, edad, DNI, usuario y contraseña, sin requerir código médico. Si
  el DNI ya existe, la cuenta se vincula al paciente registrado; si no, el sistema
  crea el registro con código automático (P001, P002...).
- Registro nuevo de profesionales, ventas/enfermería y triaje desde su acceso:
  se solicitan nombre, edad, DNI de 8 dígitos y código médico secreto; el sistema
  asigna automáticamente el código CMP, MTF o FAM correspondiente.
- Área de ventas con el portal actual de enfermería: citas asignadas al personal
  registrado con especialidad de enfermería, indicadores, stock y ventas.
- Área de triaje con inicio de sesión independiente, agenda de citas regulares y
  registro de signos vitales por el personal técnico.
- Registro de medicamentos por lote, consulta de existencias vigentes y venta
  con descuento automático del stock. El formulario ofrece cuatro nombres de
  medicamento y 40 principios activos; al elegir Paracetamol, Ibuprofeno,
  Amoxicilina o Loratadina, completa el principio activo correspondiente.
  El número de lote se escribe directamente; se solicita la fecha de
  vencimiento en formato DD/MM/AAAA y no se aceptan vencimientos anteriores al
  día actual. Cada venta queda vinculada al código del paciente y guarda el
  precio, la cantidad, el usuario responsable y su fecha y hora.
- Los campos de fecha aceptan ocho dígitos y colocan automáticamente las barras
  en formato DD/MM/AAAA.
- La cita regular se agenda con personal técnico de triaje; durante la atención
  se registran signos vitales y uno de cinco niveles de prioridad. Al guardar la
  valoración, el sistema agenda una consulta con Medicina General y da prioridad
  a los niveles 1 y 2, reprogramando una cita ordinaria cuando haga falta.
- La cita directa permite elegir un área de atención y muestra a los
  profesionales cuyas especialidades pertenecen a esa área. Las especialidades
  se seleccionan desde el catálogo compartido al registrar profesionales.
- El triaje guarda temperatura, presión arterial, frecuencia cardíaca, saturación
  de oxígeno, peso, talla y el nivel 1–5 seleccionado por el técnico. Los niveles
  1 y 2 reciben prioridad de Medicina General; si corresponde, el médico general
  puede indicar una derivación urgente a un especialista.
- El motivo de una cita puede incluir varios síntomas de la lista o un síntoma
  personalizado.
- En ambas modalidades se guardan por separado la fecha y hora de generación y
  las de atención. Los turnos duran 20 minutos.
- Las derivaciones desde Medicina General se limitan a los niveles de triaje 1 y
  2. El área que corresponde se elige tras el diagnóstico, y el sistema agenda la
  cita urgente con el especialista elegido.
- El profesional cuenta con vistas separadas para sus atenciones de hoy y su
  historial de atenciones finalizadas o derivadas.
- Los turnos pasan automáticamente a «En proceso» al comenzar. Al finalizar el
  turno sin opinión médica o sin derivación se marcan «No atendida»; las derivaciones permanecen
  «En proceso» hasta que el profesional receptor registra el veredicto final.
- La administración puede consultar el historial de ventas de farmacia dentro
  de Gestión de enfermería.
- Recetas por atención médica con medicamento, duración en días y frecuencia;
  aparecen junto con las ventas vinculadas en el historial clínico del paciente.
- Aceptación obligatoria de los términos y condiciones al crear una cuenta;
  el texto completo se consulta desde el formulario. El inicio de sesión no
  solicita esta aceptación.
- Búsqueda rápida administrativa por código o DNI de pacientes y personal
  profesional o de enfermería.
- Resultados de búsqueda con los datos del paciente, sus citas y atenciones,
  el profesional que lo atendió y el diagnóstico registrado. El DNI se muestra
  enmascarado.
- La búsqueda rápida acepta códigos de 2 o más caracteres y DNI de 8 dígitos.
  Los valores de ocho dígitos se comprueban tanto como código como DNI. Si no
  hay coincidencias, muestra un aviso en el panel sin abrir la pantalla de
  resultados.
- Pantalla interna de resultados con botón **← Volver**; el panel administrativo
  queda oculto mientras se consulta el resultado.
- Registro, consulta, cancelación y reprogramación de citas.
- Registro y actualización de atenciones médicas e historiales clínicos.
- Turnos de 20 minutos entre las 07:00 y las 18:00; el último turno comienza a
  las 17:40. El sistema rechaza citas pasadas y evita reservar el mismo horario
  para un profesional.
- Cancelación automática de citas pendientes o reprogramadas que ya vencieron.
- Reportes y estadísticas básicas del establecimiento.
- Desplazamiento vertical con la barra, la rueda del mouse y el touchpad en las
  pantallas largas, incluido el panel administrativo.
  El touchpad de laptop se desplaza con suavidad; la sensibilidad se ajusta con
  `SENSIBILIDAD_TOUCHPAD` y `PIXELES_POR_CLIC` al inicio de `interfaz/navegacion.py`.
- Navegación dentro de una sola ventana raíz. **Alt+←** vuelve a la pantalla
  anterior, **Alt+Inicio** regresa al inicio y **F11** alterna la pantalla
  completa.
- Los formularios de acceso y términos se muestran dentro de la ventana
  principal. Los formularios de atención y reprogramación del profesional
  también se muestran como vistas internas; las pantallas largas usan
  desplazamiento vertical al reducir la ventana.
- Validación de datos y manejo de errores.
- Protección de DNI con PBKDF2-HMAC-SHA256 y una sal aleatoria.

## 2. Paradigmas aplicados

- **Programación orientada a objetos:** modelos de dominio, herencia,
  encapsulamiento y coordinación de operaciones del sistema.
- **Programación funcional:** uso de `map`, `filter`, `lambda` y procesamiento
  de colecciones.
- **Programación orientada a eventos:** botones, teclado y eventos de Tkinter.

## 3. Patrones de diseño

- **Singleton:** `GestorBaseDatos` administra las conexiones a SQLite.
- **Factory:** `FabricaEntidades` centraliza la creación de pacientes,
  profesionales, citas y atenciones.

## 4. Arquitectura

```text
SistemaRural-PE/
├── interfaz/
│   ├── pantalla_inicio.py
│   ├── pantalla_paciente.py
│   ├── citas_paciente.py
│   ├── pantalla_profesional.py
│   ├── pantalla_enfermeria.py
│   ├── pantalla_triaje.py
│   ├── pantalla_administrativa.py
│   ├── campos/
│   │   └── fecha.py
│   ├── estilos/
│   │   ├── paleta.py
│   │   ├── ventana.py
│   │   └── widgets.py
│   └── navegacion/
│       ├── atajos.py
│       └── desplazamiento.py
├── componentes/
│   └── modal_verificador.py
├── modelos/
│   ├── persona.py
│   ├── personal.py
│   ├── personal_enfermeria.py
│   ├── paciente.py
│   ├── personal_salud.py
│   ├── cita.py
│   ├── atencion_medica.py
│   ├── valoracion_triaje.py
│   ├── especialidades.py
│   └── medicamento_recetado.py
├── servicios/
│   ├── sistema_salud.py
│   ├── repositorio.py
│   ├── gestor_bd.py
│   ├── fabrica.py
│   ├── contratos.py
│   ├── autenticacion.py
│   ├── validaciones.py
│   ├── reportes.py
│   └── seguridad/
│       ├── constantes.py
│       └── seguridad.py
├── pruebas/
│   ├── test_sistema.py
│   ├── test_patrones.py
│   ├── test_desplazamiento.py
│   └── test_citas_paciente.py
├── datos/                  (salud.db se crea al ejecutar)
├── imagenes/
│   └── icono_inicio.png
├── main.py
├── requirements.txt
└── README.md
```

## 5. Instalación

Se recomienda Python 3.10 o posterior y el uso de un entorno virtual.

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 6. Ejecución

```powershell
python main.py
```

La aplicación se abre en una sola ventana. Las pantallas internas reemplazan
temporalmente la vista anterior y utilizan **← Volver** para regresar al nivel
correspondiente.

## 7. Configuración de cuentas

- En la primera selección de **Administrativa**, crea la cuenta administrativa
  inicial. El formulario de configuración deja de aparecer después de crearla.
- Usa el panel administrativo para registrar pacientes y personal. El personal
  también puede crear su propio registro al crear una cuenta de acceso.
- En cada acceso de paciente, profesional, ventas o triaje, se puede seleccionar
  **Crear cuenta de acceso**. Para el personal, se abre un formulario para
  registro y acceso. El paciente valida su código y DNI. Profesional, ventas y
  triaje pueden vincularse a un registro existente mediante el DNI o crear uno
  nuevo; su código se genera automáticamente (CMP, MTF o FAM). Se solicita el
  código de autorización compartido `ArchiNet2026`, respetando exactamente las
  mayúsculas y minúsculas. Los campos
  de DNI aceptan exactamente 8 dígitos y los nombres solo letras, tildes, ñ y
  espacios. Todas las altas nuevas
  solicitan aceptar los términos y condiciones; el inicio de sesión de cuentas
  existentes no.
- Los roles de ventas y triaje solo se asignan a registros con especialidad de
  enfermería. El acceso administrativo es independiente y no se puede crear
  desde los formularios de paciente o personal.

## 8. Pruebas automatizadas

Ejecuta las pruebas con:

```powershell
python -m pytest
```

Las pruebas existentes cubren las operaciones principales del sistema, la
persistencia y la protección de DNI. El flujo de autenticación por roles todavía
no cuenta con pruebas automatizadas propias.

## 9. Tratamiento de datos personales

El DNI no se almacena en texto plano: se protege mediante PBKDF2-HMAC-SHA256
con una sal aleatoria. La aplicación verifica la huella protegida durante la
búsqueda y muestra el DNI enmascarado. Las contraseñas de acceso se guardan con
hash PBKDF2-HMAC-SHA256 y sal independiente; nunca se guardan como texto plano.

El sistema tiene finalidad académica y no debe considerarse una solución lista
para producción. Un despliegue real requeriría controles adicionales, como
recuperación segura de cuentas, auditoría, respaldos, políticas de conservación,
control de intentos y otras medidas de seguridad.
