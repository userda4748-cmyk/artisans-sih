import flet as ft

def top_bar(page: ft.Page):
    page.title = "top bar"
    greeting_name = ft.Text(value="Hello, user!", size=16, weight=ft.FontWeight.W_500)
    language_button = ft.IconButton(
        icon=ft.icons.Icons.LANGUAGE,
        tooltip="Change language",
    )
    
    bar_elements = ft.Row(
        controls=[
            greeting_name,
            language_button
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
    
    return bar_elements