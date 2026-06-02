# Football IQ

NFL game situation analytics web app powered by Microsoft Fabric data lake.

## Architecture

```
Frontend (Next.js + MSAL.js)         Backend (FastAPI + MSAL Python)
┌─────────────────────────┐         ┌──────────────────────────────┐
│ User logs in via Entra  │────────>│ Validates token              │
│ Gets access token       │         │ OBO exchange for Fabric SQL  │
│ Calls backend API       │         │ Queries gold schema          │
└─────────────────────────┘         └──────────────────────────────┘
                                              │
                                              ▼
                                    ┌──────────────────────┐
                                    │ Fabric SQL Endpoint  │
                                    │ lh_nfl / gold.*      │
                                    └──────────────────────┘
```

## Prerequisites

1. **Entra ID App Registration** with:
   - SPA redirect URI: `http://localhost:3000`
   - API permission: `https://database.windows.net/user_impersonation`
   - Expose an API scope (e.g. `api://<client-id>/access_as_user`)
   - Client secret for the backend OBO exchange

2. **Fabric Lakehouse** with gold schema tables populated

3. **ODBC Driver 18 for SQL Server** installed on the backend machine

## Setup

### Backend

```bash
cd football_iq/backend
cp .env.example .env
# Fill in your Entra app registration values

python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd football_iq/frontend
cp .env.local.example .env.local
# Fill in your Entra app client ID and API scope

npm install
npm run dev
```

Open http://localhost:3000, sign in, and select teams to see the situation chart.

## Features

- **Team Selector**: Choose your team and opponent
- **Game Picker**: Select from matchups in the last 2 seasons
- **Situation Chart**: Down/distance and field position play counts for a specific game
- **Average Chart**: Averaged situation data across all matchups between the two teams

## Future Extensions

- OpenAI/Foundry integration for natural language game analysis
- Contract and cap data correlation with performance
- Next Gen Stats advanced metrics overlay
- Predictive play-calling tendency models
