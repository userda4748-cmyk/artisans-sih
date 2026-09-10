import flet as ft

def bottom_nav(page: ft.Page):
    # bottom buttons
    dashboard_btn = ft.Button("dashboard", on_click=lambda e: page.go("/dashboard"))
    image_studio_btn = ft.Button("ai studio", on_click=lambda e: page.go("/image_studio"))
    catalogue_btn = ft.Button("catalogue", on_click=lambda e: page.go("/catalogue"))
    
    bottom_nav = ft.Row(
        controls = [
            dashboard_btn,
            image_studio_btn,
            catalogue_btn
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )
    
    return bottom_nav