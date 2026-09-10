import flet as ft

def bottom_nav(page: ft.Page):
    # bottom buttons
    dashboard_btn = ft.Button("dashboard", on_click=lambda e: page.push_route("/dashboard"))
    image_studio_btn = ft.Button("ai studio", on_click=lambda e: page.push_route("/image_studio"))
    catalogue_btn = ft.Button("catalogue", on_click=lambda e: page.push_route("/catalogue"))
    
    bottom_nav = ft.Row(
        controls = [
            dashboard_btn,
            image_studio_btn,
            catalogue_btn
        ]
    )
    
    return bottom_nav