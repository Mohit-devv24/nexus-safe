import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.simulation.simulator import simulator
from app.services.risk_engine import calculate_risk

app = FastAPI(
    title="NEXUS-SAFE",
    version="0.1.0",
    description="Intelligent Emergency Command & Control System",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "application": "NEXUS-SAFE",
        "status": "online",
        "version": "0.1.0",
    }

@app.websocket("/ws/live")
async def live_updates(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            telemetry = simulator.generate()
            risk = calculate_risk(telemetry)
            await websocket.send_json({
                "type": "LIVE_TELEMETRY",
                "telemetry": telemetry,
                "risk": risk,
            })
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        pass
