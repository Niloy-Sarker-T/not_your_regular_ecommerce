from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.services import ai
from app.services.serializers import serialize_cart

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/image-search", response_model=schemas.ImageSearchOut)
async def image_search(file: UploadFile = File(...), db: Session = Depends(get_db)):
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Image file is empty")
    try:
        identified = ai.identify_product_from_image(image_bytes, file.content_type or "image/jpeg")
    except Exception as exc:
        identified = file.filename or "grocery product"
        print(f"Vision identification failed, using fallback: {exc}")
    products, _ = crud.list_products(db, q=identified, limit=12)
    if not products:
        products, _ = crud.list_products(db, limit=12)
    return schemas.ImageSearchOut(identified_product=identified, products=products)


@router.post("/voice-command", response_model=schemas.VoiceCommandOut)
async def voice_command(
    file: UploadFile | None = File(default=None),
    text: str | None = Form(default=None),
    db: Session = Depends(get_db),
):
    transcript = text or ""
    if file:
        audio_bytes = await file.read()
        try:
            transcript = ai.transcribe_audio(audio_bytes, file.filename or "voice.webm", file.content_type or "audio/webm") or transcript
        except Exception as exc:
            print(f"Whisper transcription failed, using supplied text/fallback: {exc}")
    if not transcript:
        raise HTTPException(status_code=400, detail="Provide audio or text for the voice command")
    return _apply_intent(transcript, db)


@router.post("/text-command", response_model=schemas.VoiceCommandOut)
def text_command(payload: schemas.VoiceTextIn, db: Session = Depends(get_db)):
    return _apply_intent(payload.text, db)


def _apply_intent(transcript: str, db: Session) -> schemas.VoiceCommandOut:
    try:
        intent = ai.extract_intent(transcript)
    except Exception as exc:
        print(f"Gemini intent extraction failed, using heuristic fallback: {exc}")
        intent = ai.heuristic_intent(transcript)

    action = intent["intent"]
    product_name = intent.get("product")
    quantity = int(intent.get("quantity") or 1)
    products = []
    message = "Command processed."

    if action == "SEARCH":
        products, _ = crud.list_products(db, q=product_name, limit=12)
        message = f"Found {len(products)} products for {product_name or 'your search'}."
    elif action == "ADD_TO_CART":
        product = crud.search_first_product(db, product_name)
        if not product:
            message = f"I could not find {product_name or 'that product'}."
        else:
            crud.add_to_cart(db, product, quantity)
            message = f"Added {quantity} x {product.name} to cart."
    elif action == "REMOVE_FROM_CART":
        product = crud.search_first_product(db, product_name)
        if product:
            crud.remove_from_cart(db, product.id)
            message = f"Removed {product.name} from cart."
        else:
            message = f"I could not find {product_name or 'that product'}."
    elif action == "UPDATE_QUANTITY":
        product = crud.search_first_product(db, product_name)
        if product:
            crud.update_cart_quantity(db, product.id, quantity)
            message = f"Updated {product.name} quantity to {quantity}."
        else:
            message = f"I could not find {product_name or 'that product'}."
    elif action == "CHECKOUT":
        _, total, item_count = crud.cart_summary(db)
        if item_count:
            crud.clear_cart(db)
            message = f"Checkout complete for {item_count} items, total ${total:.2f}."
        else:
            message = "Your cart is empty."

    cart = serialize_cart(*crud.cart_summary(db))
    return schemas.VoiceCommandOut(
        transcript=transcript,
        intent=schemas.IntentPayload(**intent),
        message=message,
        products=products,
        cart=cart,
    )
