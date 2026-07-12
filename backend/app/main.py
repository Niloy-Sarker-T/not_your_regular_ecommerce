from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ai, cart, products
from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.seed import seed_demo_products


settings = get_settings()

app = FastAPI(title="AI Smart Ecommerce API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api")
app.include_router(cart.router, prefix="/api")
app.include_router(ai.router, prefix="/api")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_demo_products(db)


@app.get("/api/health")
def health():
    return {"status": "ok"}
