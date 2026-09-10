import flet as ft

from pageviews.image_studio import image_studio
from src.pageviews.catalogue import catalogue
from src.pageviews.dashboard import dashboard


def route_change(e: ft.RouteChangeEvent):
    page = e.page
    page.clean()
    if page.route == "/image_studio":
        image_studio(page)
    elif page.route == "/catalogue":
        catalogue(page)
    else:
        dashboard(page)


def main(page: ft.Page):
    page.title = "karigar sathi"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE_800)
    page.on_route_change = route_change
    page.go("/dashboard")


ft.run(main)