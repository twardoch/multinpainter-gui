# Helper function to convert Image to png

import io
from PIL import Image

def image_to_png(image: Image.Image) -> bytes:
    png = io.BytesIO()
    image.save(png, format="PNG")
    return png.getvalue()