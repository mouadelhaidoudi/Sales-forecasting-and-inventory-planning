# Backend

FastAPI application with one entry point: `main.py`.

From this directory:

```powershell
uv sync --locked
uv run fastapi dev main.py
```

- Health endpoint: http://localhost:8000/health
- Interactive API documentation: http://localhost:8000/docs
- Allowed frontend origin for local development: http://localhost:4200

The health endpoint checks the API process only. It does not check Supabase.
Database integration and forecasting endpoints are not implemented yet.

Copy `.env.example` to `.env` before configuring Supabase. These settings are
placeholders for the upcoming integration; the current application does not load
or use them. Keep real credentials out of Git and frontend code.

See the root README for the complete project setup.
