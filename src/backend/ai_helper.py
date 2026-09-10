import asyncio
import os
import threading

from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6Ji5sohOaqSXMbpQEbqIGa6VIMLEov8WR0wbGQu7cgZgg"))
MODEL = "gemini-1.5-turbo"


def _stream_image_description(image_path):
    uploaded_file = client.files.upload(file=image_path)
    return client.models.generate_content_stream(
        model=MODEL,
        contents=[
            f"Describe the content of this image in detail: {image_path}",
            uploaded_file,
        ],
        config={"temperature": 0.5, "max_output_tokens": 200},
    )


async def describe_image_stream(image_path):
    loop = asyncio.get_running_loop()
    chunks = asyncio.Queue()

    def read_stream():
        try:
            for response in _stream_image_description(image_path):
                text = response.text
                if text:
                    loop.call_soon_threadsafe(chunks.put_nowait, text)
        except Exception as err:
            loop.call_soon_threadsafe(chunks.put_nowait, err)
        finally:
            loop.call_soon_threadsafe(chunks.put_nowait, None)

    threading.Thread(target=read_stream, daemon=True).start()

    while True:
        chunk = await chunks.get()
        if chunk is None:
            break
        if isinstance(chunk, Exception):
            raise chunk
        yield chunk


def describe_image(image_path):
    async def collect_description():
        parts = []
        async for chunk in describe_image_stream(image_path):
            parts.append(chunk)
        return "".join(parts)

    return asyncio.run(collect_description())