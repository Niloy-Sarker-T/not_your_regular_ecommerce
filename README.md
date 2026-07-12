# Smart Grocery AI

Smart Grocery AI is a demo AI-powered e-commerce web application for grocery and FMCG products. It demonstrates a clean end-to-end shopping flow with product browsing, image-based product search, a voice shopping assistant, cart operations, and mock checkout.
## Live Demo

🚀 Live Website: https://not-your-regular-ecommerce-front.onrender.com



## Tech Stack

### Frontend

- React
- Vite
- Tailwind CSS
- React Router
- Axios
- Lucide React icons

### Backend

- FastAPI
- SQLAlchemy ORM
- Pydantic
- SQLite

### AI Integrations

- Gemini Vision API for image-based product identification
- Gemini API for structured shopping intent extraction
- OpenAI Whisper API for speech-to-text

### Data Source

- Open Food Facts for one-time product import
- Runtime product data is served from local SQLite, not from Open Food Facts

## App Flow

### Normal Shopping Flow

1. User opens the React frontend.
2. Frontend requests products from the FastAPI backend.
3. Backend reads products from SQLite.
4. User browses, searches, opens product details, and adds products to cart.
5. Cart actions are handled by backend business logic.
6. User completes a checkout, which clears the demo cart.

### Image Search Flow

1. User uploads a product image.
2. Frontend sends the image to `POST /api/ai/image-search`.
3. Backend sends the image to Gemini Vision.
4. Gemini returns a short product name or description.
5. Backend searches the local SQLite product catalog.
6. Matching products are returned to the frontend.

### Voice Shopping Flow

1. User records a voice command or types a command.
2. Audio is sent to the backend.
3. A Hugging Face-hosted Whisper model(trained for bangla STT) deployed in Spaces performs speech-to-text transcription by converting audio into text.
4. Gemini receives the text and returns structured JSON only.
5. Backend reads the JSON intent and performs the action.
6. Frontend updates products or cart state.

Supported voice intents:

```text
SEARCH
ADD_TO_CART
REMOVE_FROM_CART
UPDATE_QUANTITY
CHECKOUT
```

Example:

```json
{
  "intent": "ADD_TO_CART",
  "product": "Dove Shampoo",
  "quantity": 2
}
```

## Features

- Product listing
- Product details page
- Text product search
- Category filtering
- Shopping cart
- Add to cart
- Remove from cart
- Update cart quantity
- Mock checkout
- Image-based product search
- Voice shopping assistant
- Typed command assistant for testing
- Local SQLite product catalog
- One-time Open Food Facts import script
- Exported product JSON file

## Project Structure

```text
smart_ecommerce/
  backend/
    app/
      api/              FastAPI route modules
      services/         AI and response helper services
      config.py         Environment configuration
      crud.py           Database/business operations
      database.py       SQLite and SQLAlchemy setup
      main.py           FastAPI app entry point
      models.py         SQLAlchemy models
      schemas.py        Pydantic schemas
      seed.py           Small fallback seed catalog
    scripts/
      import_openfoodfacts.py
    products.json       Exported product catalog
    requirements.txt
  frontend/
    src/
      components/       Reusable product UI components
      pages/            Shop, cart, product detail, assistant pages
      state/            Cart context
      api.js            Axios API client
      App.jsx           App routes and shell
    vite.config.js
    package.json
```

## Database

The app uses SQLite with SQLAlchemy ORM.

Implemented tables:

```text
products
- id
- name
- brand
- category
- description
- price
- stock
- image_url

cart_items
- id
- product_id
- quantity
```

There is no user table. The cart is a single global demo cart.

## Product Data

Products are imported from Open Food Facts using:

```bash
cd backend
python scripts/import_openfoodfacts.py
```

The importer downloads a curated grocery/FMCG catalog and stores it in SQLite. It generates demo prices and stock values when needed.

The app also includes:

```text
backend/products.json
```

This file is an exported copy of the local product table.

## Environment Variables

Create `backend/.env` from `backend/.env.example`.

```env
DATABASE_URL=sqlite:///./smart_ecommerce.db
FRONTEND_ORIGIN=http://127.0.0.1:5173
GEMINI_API_KEY=
OPENAI_API_KEY=
```

Create `frontend/.env` from `frontend/.env.example`.

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

For APK or deployed frontend builds, `VITE_API_BASE_URL` must point to a hosted backend URL, not `127.0.0.1`.

## Run Locally

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts/import_openfoodfacts.py
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://127.0.0.1:5173
```

## Main API Routes

```text
GET    /api/health
GET    /api/products
GET    /api/products/{product_id}
GET    /api/cart
POST   /api/cart
PATCH  /api/cart/{product_id}
DELETE /api/cart/{product_id}
POST   /api/cart/checkout
POST   /api/ai/image-search
POST   /api/ai/voice-command
POST   /api/ai/text-command
```


- Demo fallback behavior implemented for missing AI keys
- Product catalog exported to `backend/products.json`
