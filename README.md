# AI-Powered E-commerce Demo

Modern demo e-commerce app with image-based product search and a voice shopping assistant.

## Stack

- Frontend: React, Vite, Tailwind CSS, React Router, Axios
- Backend: FastAPI, SQLAlchemy ORM, SQLite
- AI integrations: Gemini Vision API, Gemini API, Whisper API

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

If you do not run the importer, the API seeds a small local demo catalog on startup so the app is still usable.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://127.0.0.1:8000`. Override with `VITE_API_BASE_URL` in `frontend/.env`.

## API Keys To Configure Manually

Backend keys live in `backend/.env`.

- `GEMINI_API_KEY`: used for image product identification and voice intent extraction.
- `OPENAI_API_KEY`: used for Whisper speech-to-text.

Frontend runtime configuration lives in `frontend/.env`.

- `VITE_API_BASE_URL`: backend URL, normally `http://127.0.0.1:8000`.

## Import Data

`backend/scripts/import_openfoodfacts.py` downloads a curated set of products from Open Food Facts once and stores them in SQLite. Normal app execution only reads local SQLite data.

## Implemented Features

- Product listing, product details, and search
- Shopping cart with add, remove, quantity update, clear
- Mock checkout
- Image upload product search through Gemini Vision
- Voice shopping flow: microphone or typed command, Whisper transcription, Gemini JSON intent extraction, backend cart/search/checkout action
- Clean modular backend routes, services, schemas, and database layer

## Not Included By Design

- Authentication
- Payment gateway
- Admin dashboard
- Wishlist
- Reviews
- Recommendation system
