# Copilot Instructions for ma-cantine

This file provides guidance to Github Copilot (github.com/features/copilot) when working with code in this repository.

## Mission & Context

**Ma Cantine** is a French government service (beta.gouv.fr) that helps collective catering actors offer quality, healthy, and sustainable meals. The platform features diagnostics, performance tracking, and teledeclaration systems for compliance with EGalim regulations.

[Live Site](https://ma-cantine.agriculture.gouv.fr) | [Project Overview](https://beta.gouv.fr/startups/ma-cantine-egalim.html)

## Tech Stack

**Backend:**
- Python 3.11+, Django 5.1, Django REST Framework, Wagtail CMS
- PostgreSQL database, Celery for async tasks
- Sentry for error tracking, Brevo for email, S3-compatible storage

**Frontend:**
- Vue 2 (legacy, in `/frontend` with Vuetify) + Vue 3 (migration in `/2024-frontend` with Vite)
- Responsive design using DSFR (French design system)

**Dev Stack:**
- `uv` for Python dependency management (not pip)
- `npm` for frontend
- Docker Compose for containerized dev environment
- Pre-commit hooks for auto-linting

## Project Structure

```
ma-cantine/
├── api/                 # REST API (serializers, viewsets, permissions)
├── data/               # Core models, admin interface, factories
├── cms/                # Wagtail CMS integration
├── frontend/           # Legacy Vue 2 app (with Vuetify)
├── 2024-frontend/      # New Vue 3 app (with Vite) - prefer this for new work
├── macantine/          # Django settings, URLs, utils, ETL
├── opendata/           # CSV exports for data.gouv.fr
├── docs/               # Full ONBOARDING.md, celery.md, docker.md
├── Dockerfile          # Multi-stage Docker build
├── compose.yaml        # 4 services: server, db, frontend, 2024-frontend, worker
└── pyproject.toml      # Single source of truth for Python deps via uv
```

## Critical Setup Notes

### Backend

1. **Always use `uv` not `pip`**: `uv sync` manages a single virtual environment + lock file
2. **Database**: Requires PostgreSQL (3306 in Docker). Create user with `CREATEROLE CREATEDB` for tests
3. **Environment config**: Copy variables from `docs/ONBOARDING.md` into `.env` file
4. **Migrations**: Run `python manage.py migrate` after any schema change
5. **Pre-commit**: Install hooks with `pre-commit install` to auto-lint on commit

### Frontend

- Vue 2: Open SSL legacy mode required: `NODE_OPTIONS=--openssl-legacy-provider npm run serve`
- Vue 3: Modern setup with Vite: `npm run dev` (prefer for new features)
- Both require `npm ci --ignore-scripts` to install dependencies

### Running Locally

```bash
# Option A: All three servers in parallel (no migrations needed first)
./local-build.sh

# Option B: Manual - open 3 terminals
# Terminal 1: Backend
python manage.py runserver  # Django on port 8000

# Terminal 2: Vue 2 frontend (optional if not working on Vue 2)
cd frontend && NODE_OPTIONS=--openssl-legacy-provider npm run serve  # Port 8080

# Terminal 3: Vue 3 frontend
cd 2024-frontend && npm run dev  # Port 5173
```

## Coding Guidelines

**Python:**
- Follow Django conventions (see existing `data/models/`, `api/serializers/`)
- Ruff line length: 119 characters
- Ruff auto-linting enforced via pre-commit
- Use factory-boy for test data (see `data/factories/`)
- Models in `data/models/`, serializers in `api/serializers/`, views in `api/views/`

**JavaScript/Vue:**
- Vue 2 in `frontend/` uses Vuetify
- Vue 3 in `2024-frontend/` uses `@gouvminint/vue-dsfr` (French design system)
- Prettier + ESLint configured in package.json

**Database:**
- Always create migrations: `python manage.py makemigrations` → review → commit
- Tests require a database that supports concurrency (tests run in parallel)

**Common Pitfalls:**
- Don't run `python -m pip` directly (use `uv` instead)
- Node version: Use LTS; Vue 2 needs `--openssl-legacy-provider` flag
- Campaign dates hardcoded in `macantine.utils.CAMPAIGN_DATES`; use env overrides for testing
- Remember 2 frontends run simultaneously on different ports; access app via Django port (8000)

## Testing & Validation

```bash
# Python tests (with pytest)
uv run pytest data/tests/

# Pre-commit check without committing
pre-commit run --all-files

# Frontend linting
npm run lint  # (in frontend/ or 2024-frontend/)
```

## Key Files & Resources

- **Full Setup Guide**: [docs/ONBOARDING.md](../docs/ONBOARDING.md) - 400+ lines, highly detailed
- **Docker Guide**: [docs/docker.md](../docs/docker.md)
- **Celery Tasks**: [docs/celery.md](../docs/celery.md) - for async task env vars
- **API Schema**: Auto-generated OpenAPI at `/api/docs/` (drf-spectacular)
- **Configuration**: `pyproject.toml` + `.env` file (see ONBOARDING for template)
- **Deployment**: Clever Cloud via `clevercloud/` folder

## Dev Tools

- **Django shell**: `python manage.py shell` or `shell_plus` (with Django Extensions)
- **Admin interface**: http://localhost:8000/admin/ (create superuser via shell)
- **Database**: Use `psql` directly or Django ORM
- **Makefile**: Run `make docker-up` for containerized dev or `make runserver` for local Python
- **Magic auth**: Project uses custom auth tokens (see `django-magicauth` dependency)

## Important Patterns

- **Models**: Use soft deletes (`is_deleted` flag), historical tracking via `django-simple-history`
- **Permissions**: Custom permission classes in `api/permissions.py`
- **Serializers**: Camel-case API via `djangorestframework-camel-case`
- **Excel exports**: XLSX generation with `drf-excel` for reports
- **Open Data**: CSV exports in `opendata/` synced to data.gouv.fr (see `macantine/etl/open_data.py`)

## Helpful Commands

```bash
# Create Django superuser
uv run python manage.py createsuperuser

# Static files
uv run python manage.py collectstatic

# Fresh database (warning: destructive)
uv run python manage.py reset_db  # Requires django-extensions

# Translations
uv run python manage.py compilemessages  # After updating .po files
```

## When Things Break

1. **Import the secret key error**: Regenerate at https://djecrety.ir/ or use `SECRET=insecure` for dev
2. **Database permission errors**: Ensure DB user has `CREATEROLE CREATEDB`
3. **Node/npm issues**: Use `npm ci --ignore-scripts`, not `npm install`
4. **Pre-commit fails**: Run `pre-commit run --all-files` to see what's wrong, often auto-fixable
5. **Migrations conflict**: Check `data/migrations/` for merge conflicts, resolve manually

---

**Questions?** Start with [ONBOARDING.md](../docs/ONBOARDING.md) for comprehensive setup. For architecture questions, see README.md.
