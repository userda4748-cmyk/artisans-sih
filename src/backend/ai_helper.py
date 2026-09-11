import asyncio
import os
import threading
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6IgmH5zkUwcad-n-x2rNaDit5W0O6xIM8U2CJyuAhJAfA"))
MODEL = "gemini-3.8-flash"

def _stream_image_description(image_path):
    uploaded_file = client.files.upload(file=image_path)
    return client.models.generate_content_stream(
        model=MODEL,
        contents=[
            f"Describe the content of this image in detail: {image_path}",
            uploaded_file,
        ],
        config={"temperature": 0.5, "system_instruction": "You are an AI assistant for artisans that provides image descriptions for e-commerce listings."},
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

def generate_catalog_text(raw_text: str):
    """Generates bilingual catalog details and pricing suggestions."""
    prompt = f"""
    You are an e-commerce assistant for traditional Indian artisans.
    Given this item description: "{raw_text}"
    Return a response formatted exactly as follows:
    Title: <Short English Title>
    English Description: <Professional e-commerce description in English>
    Hindi Description: <Translation/Description in Hindi>
    Suggested Price: <Suggested price range in INR, e.g. 1200>
    """
    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return response.text
    except Exception as e:
        return f"Title: Handcrafted Item\nEnglish Description: {raw_text}\nHindi Description: हस्तनिर्मित उत्कृष्ट उत्पाद\nSuggested Price: 1200"