from collections import deque

BUILDING_GRAPH = {
    "Main Entrance": ["Reception", "North Corridor"],
    "Reception": ["Main Entrance", "Classroom A", "Faculty Room"],
    "Classroom A": ["Reception", "Classroom B", "Classroom C"],
    "Classroom B": ["Classroom A", "North Corridor"],
    "Classroom C": ["Classroom A", "Laboratory", "South Corridor"],
    "Laboratory": ["Classroom C", "South Corridor"],
    "Faculty Room": ["Reception", "North Corridor"],
    "North Corridor": [
        "Main Entrance", "Classroom B", "Faculty Room",
        "East Staircase", "West Staircase"
    ],
    "South Corridor": [
        "Classroom C", "Laboratory", "East Staircase",
        "West Staircase"
    ],
    "East Staircase": ["North Corridor", "South Corridor", "Exit A"],
    "West Staircase": ["North Corridor", "South Corridor", "Exit B"],
    "Exit A": ["East Staircase", "Assembly Point A"],
    "Exit B": ["West Staircase", "Assembly Point A"],
    "Assembly Point A": [],
}

VALID_ZONES = set(BUILDING_GRAPH)
EXITS = {"Exit A", "Exit B"}

def scenario_hazards(scenario: str) -> set[str]:
    hazards = {
        "NORMAL": set(),
        "RECOVERY": set(),
        "ELEVATED_RISK": {"Classroom A"},
        "FIRE": {"Laboratory", "Classroom A", "Classroom B"},
        "SMOKE_SPREAD": {"Main Entrance", "North Corridor"},
        "SENSOR_FAILURE": set(),
        "GATEWAY_FAILURE": set(),
        "BLOCKED_EXIT": set(),
        "MULTI_HAZARD": {
            "Main Entrance", "Classroom A",
            "Laboratory", "North Corridor"
        },
    }
    return hazards.get(scenario, set())

def scenario_blocked_exits(scenario: str) -> set[str]:
    if scenario == "BLOCKED_EXIT":
        return {"Exit A"}
    return set()

def find_evacuation_route(
    start: str,
    hazards: set[str],
    blocked_exits: set[str] | None = None,
) -> dict:
    if start not in VALID_ZONES:
        raise ValueError(f"Unknown starting zone: {start}")

    blocked_exits = set(blocked_exits or set()) & EXITS
    unavailable = set(hazards) | blocked_exits

    # A person already at an exit can move back inside to find
    # another exit, but a blocked exit is never a destination.
    queue = deque([(start, [start])])
    visited = {start}
    candidates = []

    while queue:
        zone, path = queue.popleft()

        if zone in EXITS and zone != start:
            if zone not in unavailable:
                candidates.append(path)
            continue

        for neighbour in BUILDING_GRAPH[zone]:
            if neighbour in visited or neighbour in unavailable:
                continue
            visited.add(neighbour)
            queue.append((neighbour, path + [neighbour]))

    if not candidates:
        return {
            "available": False,
            "route": [],
            "destination": None,
            "steps": 0,
            "message": "No available exit route found in the prototype graph.",
        }

    route = min(candidates, key=len)

    return {
        "available": True,
        "route": route,
        "destination": route[-1],
        "steps": len(route) - 1,
        "message": "Prototype route calculated; verify conditions before use.",
    }
