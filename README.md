# AI-Powered Code Generation SaaS Platform

An AI-powered SaaS platform that enables developers to build production-ready software by describing what they want to create in natural language.

## Overview

This platform guides users through a structured onboarding journey — from account creation and email verification to project input and AI-generated code review — using a clean, modern interface. The system leverages advanced AI models to translate natural language requirements into fully functional, production-ready code.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client (Next.js 14)                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  Landing    │  │  Auth Flow   │  │  Dashboard      │   │
│  │  Pages      │  │  & Onboarding│  │  & Code Review  │   │
│  └─────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              │ REST API / SSE
                              │
┌─────────────────────────────┴───────────────────────────────┐
│                    API Server (FastAPI)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │  Auth        │  │  Projects    │  │  AI Generation  │  │
│  │  Service     │  │  Service     │  │  Service        │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────┬───────────────────────────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
         ┌───────▼────────┐       ┌───────▼────────┐
         │   PostgreSQL   │       │  Redis Cache   │
         │   Database     │       │  & Queue       │
         └────────────────┘       └────────────────┘
```

## Tech Stack

### Frontend (`src/web/`)
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context + TanStack Query
- **Testing**: Vitest, Playwright

### Backend (`src/api/`)
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis
- **Task Queue**: Celery
- **AI Integration**: Anthropic Claude, OpenAI GPT-4
- **Testing**: pytest

### Infrastructure
- **Monorepo Tool**: Turborepo
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes (k8s/)
- **CI/CD**: GitHub Actions

## Monorepo Structure

```
.
├── src/
│   ├── api/              # FastAPI backend application
│   │   ├── app/
│   │   │   ├── api/      # API routes
│   │   │   ├── core/     # Core configuration
│   │   │   ├── models/   # Database models
│   │   │   ├── schemas/  # Pydantic schemas
│   │   │   ├── services/ # Business logic
│   │   │   └── tasks/    # Celery tasks
│   │   ├── tests/        # Backend tests
│   │   └── alembic/      # Database migrations
│   │
│   └── web/              # Next.js frontend application
│       ├── src/
│       │   ├── app/      # Next.js 14 App Router pages
│       │   ├── components/ # React components
│       │   ├── hooks/    # Custom React hooks
│       │   ├── contexts/ # React contexts
│       │   └── lib/      # Utility libraries
│       └── e2e/          # End-to-end tests
│
├── k8s/                  # Kubernetes manifests
│   ├── dev/
│   ├── staging/
│   ├── production/
│   └── monitoring/
│
├── .github/              # GitHub Actions workflows
├── docs/                 # Documentation
└── [config files]        # Root configuration files
```

## Prerequisites

- **Node.js**: 20.0.0 or higher
- **Python**: 3.11 or higher
- **Docker**: Latest version
- **Docker Compose**: Latest version
- **PostgreSQL**: 15+ (or use Docker)
- **Redis**: 7+ (or use Docker)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd proj_398-ai-powered-code-generation-saas-platform
```

### 2. Install Dependencies

```bash
# Install root dependencies and workspace dependencies
npm install
```

### 3. Environment Setup

Create environment files based on the examples provided:

```bash
# Backend environment
cp src/api/.env.example src/api/.env

# Frontend environment
cp src/web/.env.example src/web/.env
```

Edit the `.env` files with your configuration:
- Database credentials
- Redis connection
- API keys for AI services (Anthropic, OpenAI)
- JWT secrets
- SMTP settings for email

### 4. Start with Docker Compose

The easiest way to run the entire stack:

```bash
docker-compose up
```

This will start:
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- FastAPI backend (port 8000)
- Next.js frontend (port 3000)
- Celery worker for background tasks

### 5. Run Database Migrations

```bash
# In the backend container or locally with Python environment
cd src/api
alembic upgrade head
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Development Workflow

### Running Services Separately

#### Backend API
```bash
cd src/api
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd src/web
npm install
npm run dev
```

#### Celery Worker
```bash
cd src/api
celery -A app.core.celery_app worker --loglevel=info
```

### Using Turborepo Commands

```bash
# Run development servers for all workspaces
npm run dev

# Build all workspaces
npm run build

# Run tests across all workspaces
npm run test

# Lint all code
npm run lint

# Format code with Prettier
npm run format
```

## Testing

### Backend Tests
```bash
cd src/api
pytest
```

### Frontend Tests
```bash
cd src/web
npm run test
```

### End-to-End Tests
```bash
cd src/web
npm run test:e2e
```

## Deployment

Refer to the Kubernetes manifests in `k8s/` for deployment configurations:
- Development: `k8s/dev/`
- Staging: `k8s/staging/`
- Production: `k8s/production/`

Deployment is automated through GitHub Actions workflows in `.github/workflows/`.

## Contributing

Please read our contributing guidelines before submitting pull requests.

## License

[Your License Here]
