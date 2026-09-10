import flet as ft

from src.components.bottom_nav import bottom_nav
from src.services.camera_control import get_camera_control

def ai_studio(page: ft.Page):
    page.title = "ai studio"
    page_content = ft.Row(
        controls = [
            get_camera_control(page)
        ]
    )
    
    main_column = ft.Column(
        controls =[
            page_content,
            bottom_nav(page)
        ]
    )
    page.add(main_column)