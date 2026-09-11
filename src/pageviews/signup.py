import flet as ft

def signup_view(page: ft.Page) -> ft.Control:
    text_username = ft.TextField(label="Username", width=300)
    text_password = ft.TextField(label="Password", width=300, password=True)
    checkbox_signup = ft.Checkbox(label="I agree to terms & conditions", value=False)
    button_submit = ft.ElevatedButton("Sign Up", width=200, disabled=True)

    def validate(_e):
        button_submit.disabled = not all([
            text_username.value,
            text_password.value,
            checkbox_signup.value
        ])
        page.update()

    def submit(_e):
        if not hasattr(page, "app_data"):
            page.app_data = {}
        page.app_data["user_name"] = text_username.value
        page.go("/dashboard")

    text_username.on_change = validate
    text_password.on_change = validate
    checkbox_signup.on_change = validate
    button_submit.on_click = submit

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Karigar Sathi", size=28, weight=ft.FontWeight.BOLD, color="teal"),
                ft.Text("Create your account", size=16, color=ft.Colors.GREY_700),
                ft.Container(height=10),
                text_username,
                text_password,
                checkbox_signup,
                ft.Container(height=10),
                button_submit,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        alignment=ft.Alignment(0, 0),
        expand=True,
        padding=20,
    )