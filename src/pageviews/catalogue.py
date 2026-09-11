import flet as ft

def catalogue_view(page: ft.Page) -> ft.Control:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Auto-Cataloger", size=24, weight=ft.FontWeight.BOLD, color="teal"),
                ft.Text("Generate multilingual descriptions for your products.", size=14, color=ft.Colors.GREY_700),
                ft.Container(height=30),
                ft.Icon(ft.Icons.BOOK, size=80, color="teal"),
                ft.ElevatedButton("Create New Catalogue Entry", icon=ft.Icons.ADD),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        alignment=ft.Alignment(0, -1),
        padding=20,
        expand=True
    )