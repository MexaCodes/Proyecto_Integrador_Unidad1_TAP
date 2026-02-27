# Análisis de Interfaz: Configuración de Página y Controles de Selección

Este fragmento de código marca el inicio de una aplicación de escritorio o web construida con **Flet**, una biblioteca que permite crear interfaces en Python basadas en el ecosistema de **Flutter**. El enfoque aquí es la construcción de un formulario de registro estructurado y visualmente coherente.

### 1. Configuración del Entorno (Canvas de la Aplicación)

La función `main(page: ft.Page)` actúa como el contenedor principal de la aplicación. Las primeras líneas definen las propiedades globales del "escenario" visual:
* **Título y Color**: `page.title` establece el identificador en la pestaña del navegador o ventana. `page.bgcolor = "#FDFBE3"` utiliza un código hexadecimal para definir la estética visual (un tono crema), lo que demuestra el manejo del color en interfaces planas (Flat Design).
* **Diseño (Layout)**: `page.padding = 30` establece un margen interno para evitar que los componentes toquen los bordes de la ventana, mejorando la legibilidad y la experiencia del usuario (UX).



### 2. Manejo de Componentes de Selección (RadioGroup)

El bloque `row_genero` introduce un control de selección única conocido como **RadioGroup**. En el diseño de interfaces, este componente es crucial cuando se requiere que el usuario elija exactamente una opción de un conjunto mutuamente excluyente.

* **Estructura**: El `RadioGroup` contiene un `ft.Row`, lo que indica que las opciones se desplegarán de forma horizontal (en fila). Esta es una técnica de **Graficación 2D** aplicada a interfaces para organizar el flujo visual de izquierda a derecha.
* **Controles de Entrada**: Los objetos `ft.Radio` definen los valores posibles ("masculino", "femenino", "otro"). Cada uno cuenta con un `label` (etiqueta visual) y un `value` (valor de datos), separando la representación visual de la lógica interna de la aplicación.



### Código de Interfaz Analizado

```python
import re
import flet as ft

def main(page: ft.Page):
    # Configuración de página para entorno Web/Pyodide
    page.title = "Registro de Estudiantes - Tópicos Avanzados"
    page.bgcolor = "#FDFBE3"  # Definición cromática del fondo
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT # Modo claro para contraste

    # Contenedor para Género con selección única
    row_genero = ft.RadioGroup(
        content=ft.Row(
            controls=[
                ft.Radio(value="masculino", label="Masculino"),
                ft.Radio(value="femenino", label="Femenino"),
                ft.Radio(value="otro", label="Otro"),
            ])
    )
```

# 3. Gestión de Diálogos y Capas de Superposición (Overlay)

En el diseño de interfaces modernas, los diálogos de alerta (Alert Dialogs) actúan como una capa de comunicación crítica. El código define dos estructuras principales: una para la bienvenida y otra para la gestión de errores, utilizando un modelo de programación basado en eventos.

### Lógica de Control y Actualización de Estado

1.  **Funciones de Cierre (Callbacks)**: 
    Las funciones `cerrar_dialogo(e)` y `cerrar_error(e)` demuestran cómo se manipula el estado de la UI. Al cambiar la propiedad `.open = False`, el componente no se elimina, sino que se oculta. Es imperativo llamar a `page.update()` después de modificar el estado; en Flet, esto activa el proceso de renderizado que comunica los cambios del servidor (o script) al cliente (la ventana visual).

2.  **Configuración de AlertDialog**:
    * **welcome_dlg**: Se define como `modal=True`, lo que significa que el usuario no puede interactuar con el resto de la aplicación hasta que presione el botón "Ok". Esto es un patrón de diseño común para asegurar la lectura de información importante.
    * **Contenedores Vacíos**: El uso de `ft.Column([], ...)` permite que el contenido sea dinámico. En la lógica posterior, el programa inyectará texto o gráficos dentro de esta columna antes de abrir el diálogo.



3.  **El Concepto de Overlay**:
    La instrucción `page.overlay.append()` es vital para la organización visual. En lugar de colocar los diálogos dentro de la estructura de filas o columnas de la página (que afectaría el diseño del formulario), se envían a la capa de superposición. Esto permite que aparezcan flotando sobre cualquier otro elemento, independientemente de la posición del cursor o del scroll del usuario.

### Código de Diálogos Analizado

```python
    # Función para ocultar el diálogo de bienvenida
    def cerrar_dialogo(e):
        welcome_dlg.open = False 
        page.update()

    # Función para ocultar el diálogo de error
    def cerrar_error(e):
        dlg_error.open = False 
        page.update()
         
    # Definición de la ventana de bienvenida
    welcome_dlg = ft.AlertDialog(
        open=False, # Inicialmente oculto
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([], width=300, height=70, tight=True),
        actions=[ft.TextButton("Ok", on_click=cerrar_dialogo)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Definición de la ventana de error genérica
    dlg_error = ft.AlertDialog(
        title=ft.Text(""),
        content=ft.Text(""),
        actions=[ft.TextButton("Entendido", on_click=cerrar_error)]
    )

    # Integración a la capa superior de la página
    page.overlay.append(dlg_error)
    page.overlay.append(welcome_dlg)

```
# 4. Lógica de Validación y Procesamiento de Datos

La función `registrar_datos(e)` es el controlador principal que se activa cuando el usuario intenta enviar el formulario. Su propósito es garantizar la integridad de la información antes de procesarla, actuando como un filtro que evita el almacenamiento de datos incompletos o erróneos.

### Análisis del Algoritmo de Validación

1.  **Iteración de Campos Requeridos**:
    El código utiliza una estructura de lista de tuplas para mapear cada control (`txt_nombre`, `dd_carrera`, etc.) con un mensaje legible. Mediante un ciclo `for`, se verifica la propiedad `.value` de cada componente. Si se detecta un campo vacío, se personaliza el diálogo de error definido anteriormente y se detiene la ejecución con un `return`. Esta es una técnica de **Programación Defensiva** que mejora la robustez de la interfaz.

2.  **Validación mediante Expresiones Regulares (Regex)**:
    Una vez confirmado que los campos no están vacíos, el script aplica un patrón de búsqueda complejo: `r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'`. Esta expresión regular analiza la estructura de la cadena en `txt_email.value` para asegurar que contenga los elementos esenciales de un correo electrónico (usuario, arroba, dominio y extensión).



3.  **Construcción de la Salida y Limpieza de Estado**:
    Si todas las pruebas son superadas, se construye una cadena de texto formateada (`f-string`) que resume los datos del alumno. El sistema entonces:
    * Muestra el diálogo `welcome_dlg` con el resultado exitoso.
    * Realiza un **"Reset" de la UI**, devolviendo todos los valores a sus estados iniciales (`""` o `None`). 
    * Llama a `page.update()` para que el usuario perciba visualmente que el formulario ha sido limpiado y el registro fue exitoso.



### Código de Lógica Analizado

```python
# Función para procesar y validar el registro
def registrar_datos(e):
    nonlocal row_genero # Acceso a la variable fuera del ámbito local
    
    # Lista de validación para campos obligatorios
    validaciones = [
        (txt_nombre, "el Nombre Completo"),
        (txt_control, "el Número de Control"),
        (txt_email, "el Correo Electrónico"),
        (dd_carrera, "la Carrera"),
        (dd_semestre, "el Semestre"),
        (row_genero, "el Género")
    ]
    
    # Ciclo de revisión de integridad
    for control, nombre_error in validaciones:
        if not control.value:
            dlg_error.title = ft.Text("⚠️ Campo Requerido")
            dlg_error.content.value = f"Por favor, ingresa {nombre_error} para continuar."
            dlg_error.open = True
            page.update()
            return

    # Validación sintáctica del correo electrónico
    patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(patron_correo, txt_email.value):
        dlg_error.title = ft.Text("❌ Correo Inválido")
        dlg_error.content.value = "El formato del correo no es correcto."
        dlg_error.open = True
        page.update()
        return

    # Si todo es correcto, se muestra el éxito y se limpia la UI
    welcome_dlg.open = True
    welcome_dlg.title = ft.Text("👤 ALUMNO REGISTRADO")
    # (... limpieza de campos ...)
    page.update()
```

# 5. Controles de Entrada y Arquitectura de Contenedores

En este bloque de código se definen los elementos con los que el usuario interactuará directamente. La elección de estos controles no es arbitraria; responde a la necesidad de capturar diferentes tipos de datos (texto libre, selecciones predefinidas y retroalimentación visual) manteniendo una estética coherente mediante el uso de propiedades compartidas.

### Anatomía de los Campos de Texto (TextField)

Los objetos `txt_nombre`, `txt_control` y `txt_email` son instancias de `ft.TextField`. Este componente es la unidad básica de entrada en interfaces gráficas modernas.
* **Propiedad `label`**: Actúa como el identificador visual del campo, reemplazando la necesidad de etiquetas externas y optimizando el espacio en la interfaz.
* **Color de Borde (`#4D2A32`)**: Se utiliza una paleta de colores personalizada para reforzar la identidad visual de la aplicación, alejándose de los colores por defecto del framework para dar un acabado más profesional y diseñado.
* **Atributo `expand=True`**: Esta propiedad es vital para el diseño responsivo. Indica que el control debe ocupar todo el espacio disponible dentro de su contenedor padre (como una fila o columna), permitiendo que la interfaz se adapte automáticamente al tamaño de la ventana del navegador o de la pantalla del dispositivo.



### El Contenedor de Visualización (seccion_display)

El `seccion_display` es un `ft.Container`, un componente versátil que actúa como una "caja" con propiedades decorativas.
* **Función de Retroalimentación**: Aunque inicialmente contiene un texto vacío, su propósito es servir como un área de previsualización o depuración. 
* **Estilo Visual**: El uso de `bgcolor=ft.Colors.BLACK12` (una transparencia negra ligera) y un borde rojo (`ft.Colors.RED`) crea un contraste intencional que destaca esta sección del resto del formulario.
* **Alineación**: La propiedad `alignment` centrada asegura que cualquier contenido inyectado se posicione perfectamente en el centro geométrico del contenedor, aplicando principios de equilibrio visual en el diseño 2D.

### Selección Estructurada (Dropdown)

El componente `dd_carrera` implementa un menú desplegable, ideal para entradas de datos que deben restringirse a una lista específica de opciones.
* **Integridad de Datos**: Al usar un `Dropdown`, se eliminan errores de dedo o variaciones en los nombres de las carreras, facilitando el procesamiento posterior en bases de datos.
* **Opciones Dinámicas**: El uso de `ft.dropdown.Option` permite definir una lista de objetos que el framework renderiza como una lista emergente. Al igual que los campos de texto, este control mantiene el estilo visual mediante `border_color` y la capacidad responsiva con `expand=True`.



### Código de Componentes Analizado

```python
# --- CONTROLES DE ENTRADA (Definición de Componentes) ---

# Campos de entrada de texto con estilo personalizado y expansión responsiva
txt_nombre = ft.TextField(label="Nombre", border_color="#4D2A32", expand=True)
txt_control = ft.TextField(label="Numero de control", border_color="#4D2A32", expand=True)
txt_email = ft.TextField(label="Email", border_color="#4D2A32")

# Contenedor para visualización de estados o mensajes de depuración
seccion_display = ft.Container(
    content=ft.Text("", size=20),
    bgcolor=ft.Colors.BLACK12,
    alignment=ft.alignment.Alignment(0, 0), # Centrado perfecto
    border=ft.border.all(1, ft.Colors.RED),
    expand=True
)

# Menú desplegable para selección única de carrera
dd_carrera = ft.Dropdown(
    label="Carrera",
    expand=True,
    border_color="#4D2A32",
    options=[
        ft.dropdown.Option("Ingeniería en Sistemas"),
        ft.dropdown.Option("Ingeniería Civil"),
        ft.dropdown.Option("Ingeniería Industrial"),
        ft.dropdown.Option("Ingeniería Gestion Empresarial"),
        ft.dropdown.Option("Ingeniería Electronica"),
    ]
)
```
# 6. Selección Dinámica y Componentes de Ejecución (Botones)

En este bloque final de componentes, se introducen técnicas de optimización para la creación de interfaces, como las comprensiones de listas para llenar menús desplegables, y se define el disparador principal de la lógica del negocio: el botón de envío. Estas piezas cierran el ciclo de entrada de datos para dar paso al procesamiento.

### Optimización en la Selección de Semestre (Dropdown)

El componente `dd_semestre` utiliza una técnica de programación eficiente para generar sus opciones. En lugar de declarar manualmente cada semestre, emplea una comprensión de lista: `[ft.dropdown.Option(str(i)) for i in range(1, 9)]`.
* **Eficiencia Algorítmica**: Esta línea genera automáticamente ocho objetos de opción (del 1 al 8), reduciendo la redundancia de código y minimizando la posibilidad de errores tipográficos.
* **Consistencia Visual**: Al heredar propiedades como `expand=True` y `border_color="#4D2A32"`, se mantiene la armonía estética con los campos de nombre y carrera, asegurando que todos los elementos de selección tengan el mismo peso visual en el formulario.



### Botón de Acción y Personalización Estética (ElevatedButton)

El `btn_enviar` es el componente de control más crítico, ya que actúa como el puente entre la interfaz de usuario y la lógica de validación. Su configuración destaca por adaptarse a requerimientos específicos de diseño y versiones de la API:
* **Uso de `content`**: En lugar de usar la propiedad simple `text`, se utiliza `content=ft.Text(...)`. Esto permite un control granular sobre el estilo del texto (color negro, tamaño 16) independientemente de los estilos predeterminados del botón.
* **Geometría y Diseño Plano**: La propiedad `shape=ft.RoundedRectangleBorder(radius=0)` elimina el redondeo de las esquinas. En graficación 2D, esto se traduce en un diseño de bordes rectos (Sharp Edges) que proyecta una imagen de robustez y seriedad técnica, alineada con sistemas de registro institucionales.
* **Dinámica de Ancho**: Al asignar `width=page.width`, el botón se convierte en un elemento de bloque completo, facilitando la interacción táctil o con el cursor al proporcionar un área de clic máxima.



### Vinculación de Eventos (Event Handling)

El parámetro `on_click=registrar_datos` es la conexión final. Define que, ante el evento de interacción (clic o tap), el sistema debe invocar la función de validación que analizamos previamente. Este es un ejemplo puro de **Programación Dirigida por Eventos**, donde la interfaz permanece en estado de espera hasta que el usuario decide confirmar su entrada, disparando así la cascada de verificaciones y el eventual mensaje de éxito.

```python
# --- DEFINICIÓN DE CONTROLES FINALES ---

# Dropdown optimizado con comprensión de listas
dd_semestre = ft.Dropdown(
    label="Semestre",
    expand=True,
    border_color="#4D2A32",
    options=[ft.dropdown.Option(str(i)) for i in range(1, 9)]
)

# Botón de acción principal con estilo personalizado
btn_enviar = ft.ElevatedButton(
    content=ft.Text("Enviar", color="black", size=16),
    bgcolor=ft.Colors.GREY_500,
    width=page.width, # Adaptabilidad al ancho de página
    style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=0), # Bordes rectos
    ),
    on_click=registrar_datos # Conexión con la lógica de validación
)
```

# 7. Construcción de la Interfaz y Despliegue (Layout & View)

El paso final del desarrollo en Flet consiste en la organización espacial de los controles. La instrucción `page.add` es el comando de renderizado que toma todos los objetos definidos previamente y los inyecta en el árbol de visualización (DOM en web) para que sean visibles y funcionales.

### Jerarquía de Contenedores: Columnas y Filas

La estructura se basa en el sistema de diseño de "Flexbox", que organiza los elementos en ejes principales y secundarios:

1.  **El Contenedor Principal (ft.Column)**: 
    Actúa como el eje vertical de la aplicación. Al agrupar los campos de Nombre, Control y Email en una `Column`, se establece un orden de lectura natural de arriba hacia abajo. El parámetro `spacing=15` es fundamental para la estética; proporciona aire entre los componentes, evitando la fatiga visual y mejorando la precisión en dispositivos táctiles.

2.  **Organización Horizontal (ft.Row)**:
    Para optimizar el espacio vertical, se utiliza un `ft.Row` que contiene los menús desplegables de `dd_carrera` y `dd_semestre`. Esto crea una relación lógica entre estos dos datos (información académica) y permite que la interfaz se sienta más compacta y profesional. El `spacing=10` asegura que los bordes de los controles no se toquen, manteniendo la claridad de los campos.



3.  **Flujo del Formulario**:
    El orden en que se añaden los controles determina la **experiencia del usuario (UX)**. Al colocar los campos de texto al inicio, el grupo de radio (género) en el medio y el botón de acción al final, se sigue un flujo de trabajo lógico que culmina en el envío de la información. La sección de visualización (`seccion_display`) se mantiene comentada, lo que indica que es una herramienta de depuración que puede activarse sin alterar la estructura principal.

### Ejecución y Visualización en Navegador

La última línea del script, `ft.app(target=main, view=ft.AppView.WEB_BROWSER)`, define cómo se servirá la aplicación.
* **Target**: Indica que la función `main` es la que posee la lógica de construcción.
* **View**: Al especificar `WEB_BROWSER`, el framework inicia un servidor local y abre automáticamente una pestaña en el navegador. Esto transforma nuestro script de Python en una **Single Page Application (SPA)** moderna, capaz de ejecutarse sin necesidad de instalar componentes adicionales en el cliente, aprovechando la versatilidad de la graficación web.



### Código de Ensamblado Final

```python
# --- CONSTRUCCIÓN DE LA INTERFAZ (Ensamblado) ---
page.add(
    ft.Column([
        txt_nombre,
        txt_control,
        txt_email,
        # Fila para Carrera y Semestre (Organización paralela)
        ft.Row([
            dd_carrera,
            dd_semestre
        ], spacing=10),
        # Sección de selección de Género
        row_genero,
        # Acción principal
        btn_enviar,
    ], spacing=15) # Espaciado vertical uniforme
)

# Punto de entrada para ejecución en entorno web
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
```
# RESULTADOS
<img width="1572" height="882" alt="Screenshot 2026-02-26 190951" src="https://github.com/user-attachments/assets/50e138db-8967-48ef-a650-d5c4df90384d" />
<img width="1574" height="880" alt="Screenshot 2026-02-26 191106" src="https://github.com/user-attachments/assets/958d0e37-7016-4f61-92d3-a10f2bf450ab" />

# ERRORES
<img width="1575" height="877" alt="Screenshot 2026-02-26 191042" src="https://github.com/user-attachments/assets/5ab5af00-9fff-451b-a695-9bb64d6fad4e" />
<img width="1586" height="889" alt="Screenshot 2026-02-26 191010" src="https://github.com/user-attachments/assets/b0642368-6127-4ec7-8801-ccb0c3674d0d" />
<img width="1566" height="883" alt="Screenshot 2026-02-26 191127" src="https://github.com/user-attachments/assets/a832a51b-7a97-4fc5-974e-b23b54fa197d" />
<img width="1579" height="875" alt="Screenshot 2026-02-26 191232" src="https://github.com/user-attachments/assets/dbb5bc55-eb2b-4391-ab0f-f88a3e59bf7d" />
<img width="1559" height="877" alt="Screenshot 2026-02-26 191210" src="https://github.com/user-attachments/assets/d97b9923-5d8d-470d-b03d-29b8bb0a1c68" />
<img width="1572" height="885" alt="Screenshot 2026-02-26 191149" src="https://github.com/user-attachments/assets/3a4684e7-59e5-497b-bb49-72da7949d3bf" />
<img width="1569" height="869" alt="Screenshot 2026-02-26 191251" src="https://github.com/user-attachments/assets/b0f7be6f-57d6-4fb9-b613-33f4aa98ffd0" />


# CODIGO COMPLETO
```python
import re
import flet as ft

def main(page: ft.Page):
    # Configuración de página para entorno Web/Pyodide
    page.title = "Registro de Estudiantes - Tópicos Avanzados"
    page.bgcolor = "#FDFBE3"  # Fondo crema de la imagen
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT

    # Contenedor para Genero (Se integrará Radio posteriormente)
    # Por ahora mantenemos la estructura visual con Texto
    row_genero = ft.RadioGroup(
        content=ft.Row(
            controls=[
                ft.Radio(value ="masculino", label="Masculino"),
                ft.Radio(value ="femenino", label="Femenino"),
                ft.Radio(value ="otro", label="Otro"),
            ])
    )

    def cerrar_dialogo(e):
        welcome_dlg.open = False 
        page.update()

    def cerrar_error(e):
        dlg_error.open = False 
        page.update()
         
    welcome_dlg = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([], width=300, height=70, tight=True),
        actions=[ft.TextButton("Ok", on_click=cerrar_dialogo)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    dlg_error = ft.AlertDialog(
        title=ft.Text(""),
        content=ft.Text(""),
        actions=[ft.TextButton("Entendido", on_click=cerrar_error)]
    )

    page.overlay.append(dlg_error)
    page.overlay.append(welcome_dlg)

    def registrar_datos(e):
        nonlocal row_genero
        # Validamos que no estén vacíos
        # Creamos una lista de tuplas: (Control, Nombre del campo para el mensaje)
        validaciones = [
            (txt_nombre, "el Nombre Completo"),
            (txt_control, "el Número de Control"),
            (txt_email, "el Correo Electrónico"),
            (dd_carrera, "la Carrera"),
            (dd_semestre, "el Semestre"),
            (row_genero, "el Género")
        ]
        # Revisamos uno por uno
        for control, nombre_error in validaciones:
            dlg_error.title=ft.Text("⚠️ Campo Requerido")
            if not control.value:
                # Personalizamos el mensaje del diálogo
                dlg_error.content.value = f"Por favor, ingresa {nombre_error} para continuar."
                dlg_error.open = True
                page.update()
                return
        else:
            patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(patron_correo, txt_email.value):
                dlg_error.title = ft.Text("❌ Correo Inválido")
                dlg_error.content.value = "El formato del correo no es correcto. Ejemplo: usuario@dominio.com"
                dlg_error.open = True
                page.update()
                return # <--- Si el correo está mal, nos salimos y no registramos
            # ----------------------------  
            resultado = (
                f"👤 ALUMNO REGISTRADO:\n"
                f"N.Control: {txt_control.value}\n"
                f"Nombre: {txt_nombre.value}\n"
                f"Correo: {txt_email.value}\n"
                f"Carrera: {dd_carrera.value}\n"
                f"Semestre: {dd_semestre.value}\n"
                f"Genero: {row_genero.value}"
            )
            welcome_dlg.open=True
            welcome_dlg.title = ft.Text(resultado)
            # Limpiamos los campos después de registrar
            txt_nombre.value = ""
            txt_email.value = ""
            txt_control.value = ""
            dd_carrera.value = None
            dd_semestre.value = None
            row_genero.value = None
        
        page.update() 

    # --- CONTROLES DE ENTRADA (Subtema 1.4) ---
    txt_nombre = ft.TextField(label="Nombre", border_color="#4D2A32",expand=True)
    txt_control = ft.TextField(label="Numero de control", border_color="#4D2A32", expand=True)
    txt_email = ft.TextField(label="Email", border_color="#4D2A32")

    seccion_display = ft.Container(
        content=ft.Text("", size = 20),
        bgcolor=ft.Colors.BLACK12,
        alignment=ft.alignment.Alignment(0, 0),
        border=ft.border.all(1, ft.Colors.RED),
        expand=True
    )

    dd_carrera = ft.Dropdown(
        label="Carrera",
        expand=True,
        border_color="#4D2A32",
        options=[
            ft.dropdown.Option("Ingeniería en Sistemas"),
            ft.dropdown.Option("Ingeniería Civil"),
            ft.dropdown.Option("Ingeniería Industrial"),
            ft.dropdown.Option("Ingeniería Gestion Empresarial"),
            ft.dropdown.Option("Ingeniería Electronica"),
        ]
    )

    dd_semestre = ft.Dropdown(
        label="Semestre",
        expand=True,
        border_color="#4D2A32",
        options=[ft.dropdown.Option(str(i)) for i in range(1, 9)]
    )
    
    # Campos que se integrarán como Dropdowns posteriormente
    txt_carrera = ft.TextField(label="Carrera", expand=True, border_color="#4D2A32")
    txt_semestre = ft.TextField(label="Semestre", expand=True, border_color="#4D2A32")

    # Botón Enviar adaptado a versión 0.80.6.dev (usando content)
    btn_enviar = ft.ElevatedButton(
        content=ft.Text("Enviar", color="black", size=16),
        bgcolor=ft.Colors.GREY_500,
        width=page.width, # Ocupa el ancho disponible
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0),
        ),
        on_click=registrar_datos
    )

    # --- CONSTRUCCIÓN DE LA INTERFAZ (Subtema 1.1) ---
    page.add(
        ft.Column([
            txt_nombre,
            txt_control,
            txt_email,
            # Fila para Carrera y Semestre
            ft.Row([
                dd_carrera,
                dd_semestre
            ], spacing=10),
            # Espacio para el Genero
            row_genero,
            # Botón final
            btn_enviar,
            #seccion_display
        ], spacing=15)
    )



# Ejecución específica para visualización en Navegador
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
```






