from app.models import CartItem
from app.schemas import CartItemOut, CartOut, ProductOut


def serialize_cart(items: list[CartItem], total: float, item_count: int) -> CartOut:
    return CartOut(
        items=[
            CartItemOut(
                id=item.id,
                product=ProductOut.model_validate(item.product),
                quantity=item.quantity,
                line_total=round(item.quantity * item.product.price, 2),
            )
            for item in items
        ],
        total=total,
        item_count=item_count,
    )
