import flet as ft

from src.components.bottom_nav import bottom_nav

def catalogue(page: ft.Page):
    page.title = "catalogue"
    page_content = ft.Row()
    
    main_column = ft.Column(
        controls =[
            page_content,
            bottom_nav(page)
        ]
    )
    page.add(main_column)