import os
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import flet as ft
from src.pageviews.signup import signup_view
from src.pageviews.image_studio import image_studio_view
from src.pageviews.catalogue import catalogue_view
from src.pageviews.dashboard import dashboard_view
from src.components.bottom_nav import custom_bottom_nav
from src.components.top_bar import top_bar

def route_change(e: ft.RouteChangeEvent):
    page = e.page
    page.controls.clear()

    # Read persistent state dictionary attached to page
    if not hasattr(page, "app_data"):
        page.app_data = {"user_name": None, "products": []}

    username = page.app_data.get("user_name")

    # Direct user to signup if unauthenticated
    if not username and page.route != "/signup":
        page.go("/signup")
        return

    if page.route == "/signup":
        page.add(signup_view(page))
    else:
        if page.route == "/image_studio":
            body = image_studio_view(page)
        elif page.route == "/catalogue":
            body = catalogue_view(page)
        else:
            body = dashboard_view(page)

        main_layout = ft.Column(
            controls=[
                top_bar(page),
                ft.Container(content=body, expand=True),
                custom_bottom_nav(page, page.route)
            ],
            spacing=0,
            expand=True
        )
        page.add(main_layout)

    page.update()

def main(page: ft.Page):
    page.title = "Karigar Sathi"
    page.window.width = 390
    page.window.height = 750
    page.window.resizable = True
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)

    # Persistent global application state dictionary
    page.app_data = {"user_name": None, "products": []}

    page.on_route_change = route_change
    page.go("/signup")

if __name__ == "__main__":
    ft.app(target=main)