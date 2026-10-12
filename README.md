# NEXUS-SAFE

Intelligent Emergency Command & Control System.

## Phase 1

- FastAPI backend
- SQLite-ready architecture
- Deterministic emergency simulator
- Live WebSocket telemetry
- Deterministic explainable risk engine
- Interactive Digital Twin
- Emergency scenario selector
- Responsive dashboard
- Explicit sensor communication states

## Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API: http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs

## Frontend

In a second terminal:

```bash
cd frontend
python3 -m http.server 5500
```

Open http://127.0.0.1:5500

## Simulation

NORMAL, ELEVATED_RISK, FIRE, SMOKE_SPREAD, SENSOR_FAILURE, GATEWAY_FAILURE, BLOCKED_EXIT, MULTI_HAZARD, RECOVERY.

This is a local development simulation. No real emergency calls or real-world emergency actions are performed.
