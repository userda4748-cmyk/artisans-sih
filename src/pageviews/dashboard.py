import flet as ft

def dashboard_view(page: ft.Page) -> ft.Control:
    app_data = getattr(page, "app_data", {})
    username = app_data.get("user_name", "Artisan")
    products = app_data.get("products", [])

    def logout(_e):
        if hasattr(page, "app_data"):
            page.app_data["user_name"] = None
        page.go("/signup")

    product_cards = []
    if products:
        cards = []
        for idx, img_b64 in enumerate(products):
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Image(
                                src=img_b64,
                                height=120,
                                fit=ft.BoxFit.COVER,
                                border_radius=ft.BorderRadius(8, 8, 0, 0),
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(f"Product #{idx + 1}", weight=ft.FontWeight.BOLD, size=14),
                                        ft.Text("Handcrafted Item", size=11, color=ft.Colors.GREY_600),
                                    ],
                                    spacing=2,
                                ),
                                padding=8,
                            )
                        ],
                        spacing=0,
                    ),
                ),
                width=160,
            )
            cards.append(card)

        product_cards.append(ft.Text("Your Product Catalog", size=16, weight=ft.FontWeight.BOLD))
        product_cards.append(
            ft.Row(
                controls=cards,
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
            )
        )
    else:
        product_cards.append(
            ft.Container(
                content=ft.Text("No products added yet. Use the camera button below to snap your first product!", size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                padding=15,
            )
        )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(f"Namaste, {username}!", size=24, weight=ft.FontWeight.BOLD, color="teal"),
                ft.Text("Manage your inventory and AI sales tools.", size=13, color=ft.Colors.GREY_700),
                ft.Container(height=10),
                *product_cards,
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Open Auto-Cataloger",
                    icon=ft.Icons.TRANSLATE,
                    width=260,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=lambda _: page.go("/catalogue")
                ),
                ft.ElevatedButton(
                    "Logout / Switch Account",
                    icon=ft.Icons.LOGOUT,
                    width=260,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=logout
                ),
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=15,
        alignment=ft.Alignment(0, -1),
        expand=True
    )