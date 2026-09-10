import asyncio
import base64

import flet as ft

from src.backend.remove_bg import remove_background
from src.components.bottom_nav import bottom_nav
from src.services.camera_control import get_camera_control


def image_studio(page: ft.Page):
    page.title = "image studio"

    uploaded_image = ft.Image(
        src="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wIAAgMBAp0YVwAAAABJRU5ErkJggg==",
        fit=ft.BoxFit.CONTAIN,
        visible=False,
        height=220,
        border_radius=12,
    )
    upload_status = ft.Text(visible=False, size=13, weight=ft.FontWeight.W_500)
    upload_indicator = ft.ProgressRing(visible=False, width=24, height=24)
    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    async def upload_image(_e):
        files = await file_picker.pick_files(
            dialog_title="Choose an image",
            file_type=ft.FilePickerFileType.IMAGE,
            allowed_extensions=["jpg", "jpeg", "png", "webp"],
            with_data=True,
        )
        if not files:
            return

        selected_file = files[0]
        if selected_file.bytes is None:
            upload_status.value = "Could not read the selected image."
            upload_status.visible = True
            page.update()
            return

        upload_indicator.visible = True
        upload_status.value = "AI is removing background..."
        upload_status.visible = True
        page.update()

        try:
            processed_png_bytes = await asyncio.to_thread(
                remove_background, selected_file.bytes
            )
            uploaded_image.src = base64.b64encode(processed_png_bytes).decode("ascii")
            uploaded_image.visible = True
            upload_status.value = "Background removed!"
        except Exception as err:
            upload_status.value = f"Error: {err}"
        finally:
            upload_indicator.visible = False
            page.update()

    capture_camera = ft.Row(
        controls=[
            get_camera_control(page)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    upload_image_btn = ft.Button("Upload Image", on_click=upload_image)

    page_content = ft.Column(
        controls=[
            capture_camera,
            upload_image_btn
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    upload_result = ft.Column(
        controls=[
            ft.Row(
                controls=[upload_indicator, upload_status],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=12,
            ),
            ft.Container(
                content=uploaded_image,
                alignment=ft.Alignment.CENTER,
                margin=ft.Margin.only(top=8),
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    main_column = ft.Column(
        controls=[
            page_content,
            upload_result,
            bottom_nav(page)
        ]
    )
    page.add(main_column)