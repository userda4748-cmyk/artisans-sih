import base64
import asyncio
import flet as ft
import flet_camera as fc

from src.backend.remove_bg import remove_background

def image_studio_view(page: ft.Page) -> ft.Control:
    camera_preview = fc.Camera(expand=True)

    captured_image = ft.Image(
        src="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wIAAgMBAp0YVwAAAABJRU5ErkJggg==",
        fit=ft.BoxFit.CONTAIN,
        visible=False,
        height=180,
        border_radius=8,
    )
    loading_indicator = ft.ProgressRing(visible=False, width=24, height=24)
    status_text = ft.Text(visible=False, size=13)

    async def init_camera():
        cameras = await camera_preview.get_available_cameras()
        if cameras:
            await camera_preview.initialize(
                description=cameras[0],
                resolution_preset=fc.ResolutionPreset.MEDIUM,
            )
        page.update()

    async def take_photo(_e):
        loading_indicator.visible = True
        status_text.value = "Removing background..."
        status_text.visible = True
        page.update()

        try:
            data = await camera_preview.take_picture()
            if not data:
                status_text.value = "No image was captured."
                return

            processed_png_bytes = await asyncio.to_thread(remove_background, data)
            base64_str = base64.b64encode(processed_png_bytes).decode("ascii")
            
            # Save into global app_data
            if not hasattr(page, "app_data"):
                page.app_data = {"user_name": "Artisan", "products": []}
            if "products" not in page.app_data:
                page.app_data["products"] = []

            page.app_data["products"].append(base64_str)

            captured_image.src = base64_str
            captured_image.visible = True
            status_text.value = "Background removed. Image added to Dashboard."
        except Exception as err:
            status_text.value = f"Background removal failed: {err}"
        finally:
            loading_indicator.visible = False
            page.update()

    page.run_task(init_camera)

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("AI Image Studio", size=22, weight=ft.FontWeight.BOLD, color="teal"),
                ft.Text("Capture your product image below", size=13, color=ft.Colors.GREY_700),
                ft.Container(
                    content=camera_preview,
                    height=280,
                    bgcolor=ft.Colors.BLACK,
                    border_radius=12,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                ),
                ft.FloatingActionButton(
                    icon=ft.Icons.CAMERA,
                    bgcolor="teal",
                    foreground_color="white",
                    tooltip="Take photo",
                    on_click=take_photo,
                ),
                ft.Row(
                    controls=[loading_indicator, status_text],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                captured_image,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        ),
        alignment=ft.Alignment(0, -1),
        padding=15,
        expand=True,
    )