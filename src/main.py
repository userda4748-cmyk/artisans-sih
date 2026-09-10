import flet as ft

from src.pageviews.dashboard import dashboard

def main(page: ft.Page):
    page.title = "karigar sathi"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE_800)
    dashboard(page)
ft.run(main)