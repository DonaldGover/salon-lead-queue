# Salon Lead Queue System

A production-ready business lead management and prioritization API built with FastAPI, PostgreSQL, and HTMX.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- **Smart Lead Scoring** - Weighted algorithm calculates priority based on value, urgency, and client relationship
- **Priority Queue Management** - Auto-sort or manual drag-and-drop reordering
- **RESTful API** - Full CRUD operations with OpenAPI documentation
- **Real-time Dashboard** - HTMX-powered interface with live updates
- **Activity Audit Trail** - Complete history of all changes and interactions
- **Soft Delete** - Data preservation for compliance and recovery

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI + Python 3.10+ |
| Database | PostgreSQL + SQLAlchemy ORM |
| Validation | Pydantic v2 |
| Frontend | HTMX + Jinja2 + Bootstrap 5 |
| Server | Uvicorn ASGI |

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/yourusername/salon-lead-queue.git
cd salon-lead-queue
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 3. Run

```bash
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for API documentation or http://localhost:8000/dashboard for the web interface.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/leads` | Create lead |
| GET | `/leads` | List leads (paginated) |
| GET | `/leads/{id}` | Get single lead |
| PUT | `/leads/{id}` | Update lead |
| DELETE | `/leads/{id}` | Soft delete lead |
| PUT | `/leads/{id}/reorder` | Move in queue |
| GET | `/queue` | Get prioritized queue |
| POST | `/queue/reprioritize` | Auto-sort by score |
| GET | `/queue/stats` | Queue metrics |
| GET | `/dashboard` | Web interface |

## Scoring Algorithm

Leads are scored 0-100 using weighted factors:

```
Score = (Value × 0.35) + (Urgency × 0.25) + (Tier × 0.20) +
        (Budget × 0.15) + (Strategic × 0.05)
```

| Factor | Weight | Scoring |
|--------|--------|---------|
| Estimated Value | 35% | $100k+=100, $50k+=80, $20k+=60, $5k+=40, $0+=20 |
| Urgency Level | 25% | Level × 20 (1-5 scale) |
| Client Tier | 20% | Strategic=100, Existing=70, New=40 |
| Budget Confirmed | 15% | Yes=100, No=0 |
| Strategic Fit | 5% | Yes=100, No=0 |

## Project Structure

```
salon-lead-queue/
├── app/
│   ├── main.py              # FastAPI application factory
│   ├── config.py            # Environment configuration
│   ├── database.py          # PostgreSQL connection
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic validation
│   ├── crud.py              # Database operations
│   ├── services/
│   │   ├── scoring.py       # Lead scoring algorithm
│   │   └── prioritization.py # Queue management
│   ├── routers/
│   │   ├── health.py        # Health endpoints
│   │   ├── leads.py         # Lead CRUD
│   │   ├── queue.py         # Queue management
│   │   └── dashboard.py     # HTML frontend
│   └── templates/           # Jinja2 templates
├── requirements.txt
├── .env.example
└── README.md
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server bind address | `127.0.0.1` |
| `PORT` | Server port | `8000` |
| `DATABASE_URL` | PostgreSQL connection string | - |
| `DEBUG` | Enable debug mode | `false` |

## Development

```bash
# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0

# Run tests
pytest

# Type checking
mypy app/
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Systemd Service

```ini
[Unit]
Description=Salon Lead Queue API
After=network.target postgresql.service

[Service]
User=www-data
WorkingDirectory=/opt/salon-lead-queue
Environment="DATABASE_URL=postgresql://..."
ExecStart=/opt/salon-lead-queue/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## License

MIT License - feel free to use this project for any purpose.

## Author

Built with FastAPI and PostgreSQL.
