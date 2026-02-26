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