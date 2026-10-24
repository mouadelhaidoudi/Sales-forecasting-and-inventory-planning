# Sales forecasting and inventory planning

A project to forecast weekly product sales and help a retailer identify potential
shortages or excess inventory. Stock recommendations will state their inventory
and supplier lead-time assumptions.

## Current status

The repository contains an Angular starter application, a FastAPI backend
with a health endpoint, and a folder structure for machine learning development.
Supabase will host the PostgreSQL database.

The frontend and backend are not connected yet. Database integration, data
preparation, forecasting models and inventory recommendations are planned work.

## Stack

| Layer | Technology |
| --- | --- |
| Frontend | Angular with routing and SCSS, rendered in the browser |
| Backend API | Python and FastAPI |
| Database | PostgreSQL hosted on Supabase |
| Python dependencies | uv and `uv.lock` |
| Frontend dependencies | npm and `package-lock.json` |
| Planned ML tools | pandas, NumPy, scikit-learn, XGBoost and MLflow |

## Repository structure

- `frontend/` contains the Angular application.
- `backend/main.py` is the FastAPI entry point.
- `backend/pyproject.toml` declares the Python project and dependencies.
- `backend/.env.example` documents the upcoming Supabase settings.
- `machine-learning/src/` will contain data preparation, feature engineering,
  model training, evaluation and prediction code.
- `machine-learning/data/` is reserved for local training datasets.
- `machine-learning/models/` is reserved for saved trained models.
- `.gitignore` excludes local environments, caches and secrets. The frontend has
  its own additional ignore rules for Node dependencies and build output.

## Machine learning workflow

Machine learning development belongs in `machine-learning/`. Its three subfolders
currently contain only `.gitkeep` placeholders so Git can track them while empty.
No training scripts, datasets or trained models have been added yet.

The planned workflow is to prepare historical sales data, train and evaluate a
forecasting model, and save the trained model for later predictions. Training
will initially be launched manually, separately from web requests.

The backend will use the trained model to provide forecasts to Angular. The
integration method is still to be decided. Inventory recommendations will combine
those forecasts with stock levels, supplier lead times and inventory rules.

## Prerequisites

- Node.js 24.15 or newer within version 24; development checked with 24.22.1.
- npm, included with Node.js.
- uv, available on your terminal PATH.
- Python 3.14, as declared in the backend configuration. uv can install it when
  needed.
- A Supabase project for the upcoming database integration.

## Run locally

Open a terminal in the repository root and start the frontend:

```powershell
cd frontend
npm.cmd ci
npm.cmd start
```

Visit http://localhost:4200. Angular runs as a browser application; there is no
Angular SSR or Express server in this setup.

Open a second terminal in the repository root and start the backend:

```powershell
cd backend
uv sync --locked
uv run fastapi dev main.py
```

Visit http://localhost:8000/health for `{"status":"ok"}` and
http://localhost:8000/docs for the interactive API documentation.
Keep both terminals running. Stop either development server with Ctrl+C.

## Supabase configuration

From the `backend` directory, create your local configuration template:

```powershell
Copy-Item .env.example .env
```

Set `SUPABASE_URL` to your project's URL and `SUPABASE_SECRET_KEY` to a server-only
secret key from the Supabase dashboard. Never commit real credentials or put a
secret key in Angular. `.env` is ignored; `.env.example` contains placeholders and
is intended to be committed.

These settings are reserved for the upcoming database integration. The current
health endpoint does not load `.env`, contact Supabase or confirm database
connectivity. No database schema is created by the starter application.

## Checks

From `frontend`:

```powershell
npm.cmd run build
npm.cmd test -- --watch=false
```

With the backend server running, use a separate PowerShell terminal:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

The API currently allows browser requests from `http://localhost:4200` for local
development. Public deployment, authentication and database access rules remain
to be implemented.

## Git

Use the existing repository at the project root for the frontend, backend and
machine learning code.
Commit source files, `package-lock.json`, `uv.lock` and `.env.example`.
Dependencies, build output, virtual environments and real `.env` files stay local.
