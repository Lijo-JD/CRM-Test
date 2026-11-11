# CRM AI Web Application

This project converts the original Jupyter-based CRM assistant into a full-stack web application using FastAPI for the backend and React + TypeScript for the frontend.

The app defaults to backend port 8001 and frontend port 5174 to avoid conflicts with other local services.

## Included functionality

- Customer management
- Lead pipeline tracking
- Order and revenue overview
- Product catalog
- Employee directory
- Natural-language CRM query workflow powered by Gemini or Groq
- Dashboard summary cards and data tables

## Project structure

- `backend/` – FastAPI app and API routes
- `frontend/` – Vite React + TypeScript client
- `crm.sql` – original MySQL schema and seed data
- `crm.ipynb` – original notebook reference

## Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL server with a schema named `crm_ai` (or configure a different database name in `.env`)

## 1) Generate the app

### Linux/macOS

```bash
chmod +x generate.sh
./generate.sh
```

### Windows

```bat
generate.bat
```

This will:

- create a local virtual environment
- install backend Python dependencies
- install frontend node modules
- generate `.env` from `.env.example` if missing

## 2) Configure environment

Edit the root `.env` file and provide your database and AI credentials:

```env
PORT=8001
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=crm_ai
GEMINI_API_KEY=your_gemini_key_here
GROQ_API_KEY=your_groq_key_here
AI_PROVIDER=gemini
VITE_API_URL=http://localhost:8001/api/v1
```

## 3) Run the app

### Linux/macOS

```bash
./run.sh
```

### Windows

```bat
run.bat
```

This starts:

- backend at http://localhost:8001
- frontend at http://localhost:5174

## 4) Open the app

Visit:

- http://localhost:5174

The backend OpenAPI docs are available at:

- http://localhost:8001/docs

## 5) Testing

Backend tests can be run with:

```bash
source .venv/bin/activate
pytest backend/tests -q
```

## 6) Notebook migration notes

The original notebook logic is preserved as business rules for:

- schema discovery
- SQL generation from natural language
- SQL validation blocklist
- self-healing query retries
- CRM intent routing
- dashboard summaries

The notebook is kept as a backup reference and is no longer required to operate the application.
