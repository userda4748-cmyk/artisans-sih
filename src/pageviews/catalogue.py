import flet as ft

from src.components.bottom_nav import bottom_nav

def catalogue(page: ft.Page):
    page.title = "catalogue"
    page_content = ft.Row(
        controls=[
            ft.Text(value="Catalogue", size=20, weight=ft.FontWeight.W_500)
        ]
    )
    
    main_column = ft.Column(
        controls =[
            page_content,
            bottom_nav(page)
        ]
    )
    page.add(main_column)