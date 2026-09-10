import asyncio
import base64
import flet as ft
import flet_camera as fc

from src.backend.remove_bg import remove_background


def get_camera_control(page: ft.Page, on_captured=None) -> ft.Control:
    """Returns a container containing the camera viewfinder and AI background removal trigger."""
    camera_preview = fc.Camera(expand=True)

    captured_image = ft.Image(
        src=(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wIAAgMBAp0YVwAAAABJRU5ErkJggg=="
        ),
        fit=ft.BoxFit.CONTAIN,
        visible=False,
        height=220,
        border_radius=12,
    )

    loading_indicator = ft.ProgressRing(visible=False, width=24, height=24, color=ft.Colors.ORANGE_700)
    status_text = ft.Text(visible=False, size=13, weight=ft.FontWeight.W_500)

    async def init_camera():
        try:
            cameras = await camera_preview.get_available_cameras()
            if cameras:
                await camera_preview.initialize(
                    description=cameras[0],
                    resolution_preset=fc.ResolutionPreset.MEDIUM,
                )
        except Exception as err:
            status_text.value = f"Camera status: {err}"
            status_text.visible = True
        page.update()

    async def take_photo(e):
        loading_indicator.visible = True
        status_text.value = "AI is removing background..."
        status_text.visible = True
        page.update()

        try:
            data = await camera_preview.take_picture()
            processed_png_bytes = await asyncio.to_thread(remove_background, data)

            with open("captured_photo.png", "wb") as f:
                f.write(processed_png_bytes)

            captured_image.src = base64.b64encode(processed_png_bytes).decode("ascii")
            captured_image.visible = True
            status_text.value = "Background removed! E-commerce ready PNG created."
            if on_captured:
                on_captured(processed_png_bytes)
        except Exception as err:
            status_text.value = f"Error: {err}"
        finally:
            loading_indicator.visible = False
            page.update()

    page.run_task(init_camera)

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=camera_preview,
                    height=280,
                    bgcolor=ft.Colors.BLACK,
                    border_radius=16,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.CAMERA_ALT, size=18),
                                ft.Text("Capture & Remove Background", weight=ft.FontWeight.W_600),
                            ]),
                            on_click=take_photo,
                            bgcolor=ft.Colors.ORANGE_700,
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        ),
                        loading_indicator,
                        status_text,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12,
                ),
                ft.Container(
                    content=captured_image,
                    alignment=ft.Alignment.CENTER,
                    margin=ft.Margin.only(top=8),
                ),
            ],
            spacing=12,
        ),
        padding=12,
    )


def camprev(page: ft.Page, on_back=None):
    page.title = "AI Camera Studio - Shilp Setu"
    control = get_camera_control(page)

    header_controls = []
    if on_back:
        header_controls.append(
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                tooltip="Back to Dashboard",
                on_click=lambda e: on_back(),
            )
        )
    header_controls.append(
        ft.Text("AI Photo Studio & Background Removal", size=20, weight=ft.FontWeight.BOLD)
    )

    page.clean()
    page.add(
        ft.Column(
            controls=[
                ft.Row(controls=header_controls, alignment=ft.MainAxisAlignment.START),
                control,
            ],
            expand=True,
        )
    )
