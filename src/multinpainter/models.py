import base64
import io
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import aiohttp
import httpx
import numpy as np
import openai
from PIL import Image
from .utils import image_to_png

# 1. describe_image
async def describe_image_hf(
    image: Image.Image,
    prompt_model: str,
    hf_api_key: Optional[str] = None,
) -> str:
    headers = {"Authorization": f"Bearer {hf_api_key}"}
    api_url = f"https://api-inference.huggingface.co/models/{prompt_model}"
    png = image_to_png(image)

    async def post(api_url: str, image: bytes, headers: Dict, wait_for_model: bool = True) -> Any:
        async with aiohttp.ClientSession() as session:
            payload: Dict[str, str] = {
                "inputs": {"image": base64.b64encode(image).decode("utf-8")},
                "options": {"wait_for_model": wait_for_model},
            }
            async with session.post(api_url, headers=headers, json=payload) as response:
                if not response.ok:
                    print(response)
                    print(headers)
                inference = await response.json()
        return inference

    inference = await post(api_url, png, headers=headers)
    return inference[0].get("generated_text", "").strip()

# 2. detect_humans
def detect_humans_yolo(image: Image.Image) -> List[Tuple[int, int, int, int]]:
    from ultralytics import YOLO

    boxes = []
    model = YOLO("yolov8n.pt")
    model.classes = [0]
    model.conf = 0.6
    detection = model.predict(image)

    for box_obj in detection:
        box = box_obj.boxes.xyxy.tolist()[0]
        boxes.append((int(box[0] - 0.5), int(box[1] - 0.5), int(box[2] + 0.5), int(box[3] + 0.5)))

    return sorted(boxes, key=lambda box: box[0])

# 3. detect_faces
def detect_faces_dlib(image: Image.Image) -> Optional[Any]:
    import dlib

    face_detector = dlib.get_frontal_face_detector()
    faces = face_detector(np.array(image.convert("RGB")), 1)
    return faces[0] if faces and len(faces) else None

# 4. inpaint_square
async def inpaint_square_openai(
    image: Image.Image,
    prompt: str,
    square_size: Tuple[int, int],
    openai_api_key: Optional[str] = None,
) -> Image.Image:
    openai.api_key = openai_api_key
    png = image_to_png(image)

    response = await openai.Image.acreate_edit(
        image=png, mask=png, prompt=prompt, n=1, size=f"{square_size[0]}x{square_size[1]}"
    )
    image_url = response["data"][0]["url"]

    async with httpx.AsyncClient() as client:
        response = await client.get(image_url)

    return Image.open(io.BytesIO(response.content))


