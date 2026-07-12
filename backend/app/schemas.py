from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    brand: str
    category: str
    description: str
    price: float
    stock: int
    image_url: str


class ProductOut(ProductBase):
    id: int

    model_config = {"from_attributes": True}


class ProductList(BaseModel):
    items: list[ProductOut]
    total: int
    limit: int
    offset: int


class CartItemOut(BaseModel):
    id: int
    product: ProductOut
    quantity: int
    line_total: float

    model_config = {"from_attributes": True}


class CartOut(BaseModel):
    items: list[CartItemOut]
    total: float
    item_count: int


class CartAdd(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1, le=99)


class CartUpdate(BaseModel):
    quantity: int = Field(ge=0, le=99)


class CheckoutOut(BaseModel):
    message: str
    total: float
    item_count: int


class VoiceTextIn(BaseModel):
    text: str


class IntentPayload(BaseModel):
    intent: str
    product: str | None = None
    quantity: int | None = None


class VoiceCommandOut(BaseModel):
    transcript: str
    intent: IntentPayload
    message: str
    products: list[ProductOut] = []
    cart: CartOut | None = None


class ImageSearchOut(BaseModel):
    identified_product: str
    products: list[ProductOut]
