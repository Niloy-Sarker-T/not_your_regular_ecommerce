# import base64
# import json
# import re
# from typing import Any

# import requests

# from app.config import get_settings


# INTENTS = {"SEARCH", "ADD_TO_CART", "REMOVE_FROM_CART", "UPDATE_QUANTITY", "CHECKOUT"}


# def _extract_json(text: str) -> dict[str, Any]:
#     match = re.search(r"\{.*\}", text, re.DOTALL)
#     payload = match.group(0) if match else text
#     data = json.loads(payload)
#     intent = str(data.get("intent", "SEARCH")).upper()
#     return {
#         "intent": intent if intent in INTENTS else "SEARCH",
#         "product": data.get("product"),
#         "quantity": data.get("quantity"),
#     }


# def transcribe_audio(audio_bytes: bytes, filename: str, content_type: str) -> str:
#     settings = get_settings()
#     if not settings.openai_api_key:
#         return ""

#     response = requests.post(
#         "https://api.openai.com/v1/audio/transcriptions",
#         headers={"Authorization": f"Bearer {settings.openai_api_key}"},
#         files={"file": (filename or "voice.webm", audio_bytes, content_type or "audio/webm")},
#         data={"model": "whisper-1"},
#         timeout=45,
#     )
#     response.raise_for_status()
#     return response.json().get("text", "")


# # def identify_product_from_image(image_bytes: bytes, mime_type: str) -> str:
# #     settings = get_settings()
# #     if not settings.gemini_api_key:
# #         return "grocery product"

# #     encoded = base64.b64encode(image_bytes).decode("utf-8")
# #     payload = {
# #         "contents": [
# #             {
# #                 "parts": [
# #                     {
# #                         "text": (
# #                             "Identify the grocery, FMCG, household, or personal-care product in this image. "
# #                             "Return only a short searchable product name, with brand if visible."
# #                         )
# #                     },
# #                     {"inline_data": {"mime_type": mime_type or "image/jpeg", "data": encoded}},
# #                 ]
# #             }
# #         ]
# #     }
# #     response = requests.post(
# #         "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
# #         params={"key": settings.gemini_api_key},
# #         json=payload,
# #         timeout=45,
# #     )
# #     response.raise_for_status()
# #     return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

    
# from google import genai

# client = genai.Client(api_key=settings.gemini_api_key)

# response = client.models.generate_content(
#     model="gemini-3.5-flash",
#     contents=[
#         "Identify the grocery product. Return only the product name.",
#         image,
#     ],
# )

# print(response.text)


# def extract_intent(text: str) -> dict[str, Any]:
#     settings = get_settings()
#     if not settings.gemini_api_key:
#         return heuristic_intent(text)

#     prompt = f"""
# You extract shopping intent from user text.
# Return valid JSON only. No markdown.
# Allowed intents: SEARCH, ADD_TO_CART, REMOVE_FROM_CART, UPDATE_QUANTITY, CHECKOUT.
# Schema: {{"intent":"SEARCH","product":"product name or null","quantity":1}}
# Use quantity 1 when omitted. Product can be null for CHECKOUT.

# User text: {text}
# """
#     payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0}}
#     response = requests.post(
#         "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
#         params={"key": settings.gemini_api_key},
#         json=payload,
#         timeout=30,
#     )
#     response.raise_for_status()
#     content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
#     return _extract_json(content)


# def heuristic_intent(text: str) -> dict[str, Any]:
#     lowered = text.lower().strip()
#     quantity = _quantity_from_text(lowered)
#     product = _clean_product_text(lowered)

#     if any(word in lowered for word in ["checkout", "place order", "buy now", "complete order"]):
#         return {"intent": "CHECKOUT", "product": None, "quantity": None}
#     if any(word in lowered for word in ["remove", "delete", "take out"]):
#         return {"intent": "REMOVE_FROM_CART", "product": product, "quantity": quantity}
#     if any(word in lowered for word in ["update", "change", "set"]) and "cart" in lowered:
#         return {"intent": "UPDATE_QUANTITY", "product": product, "quantity": quantity}
#     if any(word in lowered for word in ["add", "put"]) and "cart" in lowered:
#         return {"intent": "ADD_TO_CART", "product": product, "quantity": quantity}
#     return {"intent": "SEARCH", "product": product or text, "quantity": quantity}


# def _quantity_from_text(text: str) -> int:
#     words = {
#         "one": 1,
#         "a": 1,
#         "two": 2,
#         "three": 3,
#         "four": 4,
#         "five": 5,
#         "six": 6,
#         "seven": 7,
#         "eight": 8,
#         "nine": 9,
#         "ten": 10,
#     }
#     number = re.search(r"\b\d+\b", text)
#     if number:
#         return max(1, int(number.group(0)))
#     for word, value in words.items():
#         if re.search(rf"\b{word}\b", text):
#             return value
#     return 1


# def _clean_product_text(text: str) -> str:
#     cleaned = re.sub(r"\b(add|put|remove|delete|take out|update|change|set|search|find|show|get|to|from|my|the|cart|quantity|qty|items?|of|for|please)\b", " ", text)
#     cleaned = re.sub(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\b", " ", cleaned)
#     return re.sub(r"\s+", " ", cleaned).strip()





import io
import json
import re
from typing import Any

import requests
from PIL import Image
from google import genai

from app.config import get_settings


INTENTS = {"SEARCH", "ADD_TO_CART", "REMOVE_FROM_CART", "UPDATE_QUANTITY", "CHECKOUT"}


def _extract_json(text: str) -> dict[str, Any]:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    payload = match.group(0) if match else text
    data = json.loads(payload)
    intent = str(data.get("intent", "SEARCH")).upper()

    return {
        "intent": intent if intent in INTENTS else "SEARCH",
        "product": data.get("product"),
        "quantity": data.get("quantity"),
    }


from gradio_client import Client, handle_file
import tempfile


def transcribe_audio(audio_bytes: bytes, filename: str, content_type: str) -> str:
    settings = get_settings()

    client = Client(settings.hf_asr_space)

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False,
    ) as f:
        f.write(audio_bytes)
        temp_path = f.name

    result = client.predict(
        audio=handle_file(temp_path),
        api_name="/transcribe",
    )

    return result


def identify_product_from_image(image_bytes: bytes, mime_type: str) -> str:
    settings = get_settings()

    if not settings.gemini_api_key:
        print("No Gemini API key found.")
        return "grocery product"

    try:
        client = genai.Client(api_key=settings.gemini_api_key)

        image = Image.open(io.BytesIO(image_bytes))

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                
    """
Identify the main product shown in the image.

Return ONLY a single, generic product name that can be used to search an online grocery store.

Examples:
"Coca-Cola Original Taste" → "Coca-Cola"
"Nature's Secret Olive Oil" → "Olive Oil"
"ACI Pure Mustard Oil" → "Mustard Oil"
"Lux Soft Glow Soap" → "Soap"
"Nestlé Nescafe Classic Coffee" → "Coffee"
"Pringles Sour Cream & Onion" → "Potato Chips"

Do NOT include:
- Flavor
- Variant
- Weight
- Pack size
- Promotional text
- Brand name (unless it is essential for identifying the product, e.g., "Coca-Cola")

Return only the product name. Do not include quotes, explanations, or any other text.
"""
,
                image,
            ],
        )

        print("Gemini response:", response.text)

        if response.text:
            return response.text.strip()

        return "grocery product"

    except Exception as e:
        print("Gemini Vision Error:", e)
        return "grocery product"


def extract_intent(text: str) -> dict[str, Any]:
    settings = get_settings()

    if not settings.gemini_api_key:
        return heuristic_intent(text)

    client = genai.Client(api_key=settings.gemini_api_key)

    prompt = f"""
You extract shopping intent.

Return ONLY valid JSON.

Allowed intents:
SEARCH
ADD_TO_CART
REMOVE_FROM_CART
UPDATE_QUANTITY
CHECKOUT

Schema:
{{"intent":"SEARCH","product":"product name or null","quantity":1}}

IMPORTANT:
- Return the product name in English, even if the user speaks Bangla.
- Translate Bangla product names into their standard English grocery names.
- Quantity must be an integer.
- If quantity is omitted, use 1.
- Product can be null only for CHECKOUT.

Examples:

User:
দুইটা অলিভ অয়েল কার্টে যোগ করো

Return:
{{"intent":"ADD_TO_CART","product":"Olive Oil","quantity":2}}

User:
কোকাকোলা দেখাও

Return:
{{"intent":"SEARCH","product":"Coca-Cola","quantity":1}}

User:
লাক্স সাবান

Return:
{{"intent":"SEARCH","product":"Lux Soap","quantity":1}}

User:
{text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return _extract_json(response.text)

def heuristic_intent(text: str) -> dict[str, Any]:
    lowered = text.lower().strip()
    quantity = _quantity_from_text(lowered)
    product = _clean_product_text(lowered)

    if any(word in lowered for word in ["checkout", "place order", "buy now", "complete order"]):
        return {"intent": "CHECKOUT", "product": None, "quantity": None}

    if any(word in lowered for word in ["remove", "delete", "take out"]):
        return {
            "intent": "REMOVE_FROM_CART",
            "product": product,
            "quantity": quantity,
        }

    if any(word in lowered for word in ["update", "change", "set"]) and "cart" in lowered:
        return {
            "intent": "UPDATE_QUANTITY",
            "product": product,
            "quantity": quantity,
        }

    if any(word in lowered for word in ["add", "put"]) and "cart" in lowered:
        return {
            "intent": "ADD_TO_CART",
            "product": product,
            "quantity": quantity,
        }

    return {
        "intent": "SEARCH",
        "product": product or text,
        "quantity": quantity,
    }


def _quantity_from_text(text: str) -> int:
    words = {
        "one": 1,
        "a": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }

    number = re.search(r"\b\d+\b", text)

    if number:
        return max(1, int(number.group(0)))

    for word, value in words.items():
        if re.search(rf"\b{word}\b", text):
            return value

    return 1


def _clean_product_text(text: str) -> str:
    cleaned = re.sub(
        r"\b(add|put|remove|delete|take out|update|change|set|search|find|show|get|to|from|my|the|cart|quantity|qty|items?|of|for|please)\b",
        " ",
        text,
    )

    cleaned = re.sub(
        r"\b(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\b",
        " ",
        cleaned,
    )

    return re.sub(r"\s+", " ", cleaned).strip()