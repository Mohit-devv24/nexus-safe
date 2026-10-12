from fastapi import APIRouter, HTTPException
from app.simulation.simulator import simulator, SCENARIOS
from app.services.risk_engine import calculate_risk

router = APIRouter(prefix="/api")

@router.get("/health")
def health():
    return {
        "status": "online",
        "application": "NEXUS-SAFE",
        "simulation_mode": True,
    }

@router.get("/simulation/scenarios")
def scenarios():
    return {"scenarios": SCENARIOS, "active": simulator.scenario}

@router.post("/simulation/scenario/{scenario}")
def change_scenario(scenario: str):
    try:
        simulator.set_scenario(scenario)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"success": True, "scenario": simulator.scenario}

@router.get("/simulation/tick")
def simulation_tick():
    data = simulator.generate()
    return {"telemetry": data, "risk": calculate_risk(data)}

from fastapi import Query
from app.services.evacuation import (
    VALID_ZONES,
    scenario_hazards,
    scenario_blocked_exits,
    find_evacuation_route,
)

@router.get("/evacuation/route")
def evacuation_route(
    from_zone: str = "Classroom A",
    blocked_exits: list[str] = Query(default=[]),
):
    if from_zone not in VALID_ZONES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown zone: {from_zone}",
        )

    valid_exits = {"Exit A", "Exit B"}
    invalid_exits = set(blocked_exits) - valid_exits
    if invalid_exits:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid exits: {sorted(invalid_exits)}",
        )

    hazards = scenario_hazards(simulator.scenario)
    unavailable_exits = (
        scenario_blocked_exits(simulator.scenario)
        | set(blocked_exits)
    )

    result = find_evacuation_route(
        start=from_zone,
        hazards=hazards,
        blocked_exits=unavailable_exits,
    )

    return {
        "scenario": simulator.scenario,
        "starting_zone": from_zone,
        "hazard_zones": sorted(hazards),
        "blocked_exits": sorted(unavailable_exits),
        **result,
    }
