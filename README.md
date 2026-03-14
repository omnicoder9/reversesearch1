# Reverse Search App

A privacy-aware OSINT-style reverse search MVP that accepts partial identifiers and returns an aggregated public-profile view with confidence scores.

## Important Ethics and Legal Notice

- This project is for lawful investigations, cybersecurity, journalism, and personal digital hygiene only.
- You must have valid legal basis and consent before processing personal data.
- Do not use for harassment, stalking, discrimination, or unlawful profiling.
- Scraping many social networks may violate platform Terms of Service; use official APIs where required.
- This MVP uses **mock providers** for account/mention/photo matches. Integrate approved data sources before production use.

## Architecture (MVP)

- `frontend/`: React + Vite UI for input and dashboard.
- `backend/`: FastAPI API gateway, parser, aggregator, scoring logic.
- `worker`: Celery async task processor.
- `redis`: cache/result backend.
- `rabbitmq`: Celery broker.

Data flow:
1. User submits identifiers (`username`, `email`, `phone`, `full_name`, `photo_url`) and `consent_confirmed=true`.
2. API validates and queues async search task.
3. Worker runs search modules in parallel-style pipeline (currently mocked), aggregates and scores.
4. Frontend polls task status and renders profile dashboard + confidence chart.

## Tech Stack

- Backend: Python 3.11, FastAPI, Celery, Redis, RabbitMQ, RapidFuzz, NetworkX
- Frontend: React 18, Vite, TypeScript, Chart.js
- Infra: Docker Compose

## Environment Setup

### Prerequisites

- Docker + Docker Compose
- Optionally for local non-Docker development:
  - Python 3.11 or 3.12 recommended (3.14 is not fully supported by some dependencies yet)
  - Node.js 20+
  - `npm`

### 1) Configure Environment Files

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

`backend/.env` important keys:

- `REQUIRE_CONSENT=true`: blocks searches without explicit consent checkbox.
- `RATE_LIMIT=20/minute`: API abuse control.
- `ENABLE_MOCK_PROVIDERS=true`: keep mocked providers enabled for MVP.
- `REDIS_URL`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`: queue/cache wiring.

### 2) Run with Docker (Recommended)

```bash
docker compose up --build
```

Services:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs (Swagger): http://localhost:8000/docs
- RabbitMQ UI: http://localhost:15672 (guest/guest)

### 3) Local Development Without Docker (Optional)

Backend shell:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Worker shell:

```bash
cd backend
source .venv/bin/activate
celery -A app.workers.worker.celery_app worker --loglevel=info
```

Frontend shell:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## API Endpoints

- `POST /api/v1/search`
  - Requires at least one identifier and `consent_confirmed=true`.
  - Returns `{ task_id, status }`.
- `GET /api/v1/search/{task_id}`
  - Poll until `SUCCESS` or `FAILURE`.

## Example Request

```json
{
  "username": "john_doe",
  "platform": "github",
  "email": "john@example.com",
  "consent_confirmed": true
}
```

## Security and Compliance Guidance (Production)

- Replace mocked modules with official/approved APIs and explicit contracts.
- Add authentication (JWT/OAuth2), per-user quota policies, and CAPTCHA.
- Encrypt data in transit (TLS) and at rest where persistence is needed.
- Keep results ephemeral by default and add explicit opt-in for saved reports.
- Implement audit logs with PII minimization/anonymization.
- Add legal review for GDPR/CCPA and platform-specific ToS compliance.

## Testing

Backend unit tests:

```bash
cd backend
pytest -q
```

## Next Extension Points

- Add provider adapters in `backend/app/services/search_modules.py`
- Add ML-based confidence model replacing rules in `backend/app/services/confidence.py`
- Add PDF/CSV report export endpoint and signed download links
