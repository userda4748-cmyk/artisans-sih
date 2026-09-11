import flet as ft

def custom_bottom_nav(page: ft.Page, active_route: str = "") -> ft.Control:
    current_route = active_route or page.route

    home_color = "orange" if current_route == "/dashboard" else "white"
    cat_color = "orange" if current_route == "/catalogue" else "white"
    camera_color = "orange" if current_route == "/image_studio" else "teal"

    home_btn = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_size=32,
        icon_color=home_color,
        on_click=lambda _: page.go("/dashboard"),
    )

    cat_btn = ft.IconButton(
        icon=ft.Icons.BOOK,
        icon_size=30,
        icon_color=cat_color,
        on_click=lambda _: page.go("/catalogue"),
    )

    bullet = ft.Container(
        shape=ft.BoxShape.CIRCLE,
        bgcolor="white",
        height=65,
        width=65,
        left=162,
        bottom=20,
        border=ft.Border(
            top=ft.BorderSide(2, "teal"),
            bottom=ft.BorderSide(2, "teal"),
            left=ft.BorderSide(2, "teal"),
            right=ft.BorderSide(2, "teal"),
        ),
        alignment=ft.Alignment(0, 0),
        content=ft.Icon(ft.Icons.PHOTO_CAMERA, size=32, color=camera_color),
        on_click=lambda _: page.go("/image_studio"),
        ink=True,
    )

    nav_bar = ft.Container(
        bgcolor="teal",
        width=page.window.width,
        height=60,
        bottom=0,
        padding=ft.Padding(left=20, top=0, right=20, bottom=0),
        content=ft.Row(
            [home_btn, cat_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    return ft.Stack(
        controls=[nav_bar, bullet],
        height=85,
    )

def bottom_nav(page: ft.Page) -> ft.Control:
    return custom_bottom_nav(page, page.route)