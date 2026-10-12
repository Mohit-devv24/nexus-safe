import random
from datetime import datetime

SCENARIOS = [
    "NORMAL",
    "ELEVATED_RISK",
    "FIRE",
    "SMOKE_SPREAD",
    "SENSOR_FAILURE",
    "GATEWAY_FAILURE",
    "BLOCKED_EXIT",
    "MULTI_HAZARD",
    "RECOVERY",
]

ZONES = [
    "Main Entrance", "Reception", "Classroom A", "Classroom B",
    "Classroom C", "Laboratory", "Faculty Room", "North Corridor",
    "South Corridor", "East Staircase", "West Staircase",
    "Exit A", "Exit B", "Assembly Point A",
]

class Simulator:
    def __init__(self):
        self.scenario = "NORMAL"
        self.tick = 0

    def set_scenario(self, scenario: str):
        scenario = scenario.upper()
        if scenario not in SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}")
        self.scenario = scenario
        self.tick = 0

    def generate(self):
        self.tick += 1
        zone = random.choice(ZONES)
        temperature = random.uniform(22, 30)
        smoke = random.uniform(0, 10)
        occupancy = random.randint(5, 45)
        gas = random.uniform(0, 5)
        status = "HEALTHY"

        if self.scenario == "ELEVATED_RISK":
            temperature = random.uniform(35, 55)
            smoke = random.uniform(15, 35)
        elif self.scenario == "FIRE":
            zone = random.choice(["Laboratory", "Classroom A", "Classroom B"])
            temperature = random.uniform(70, 110)
            smoke = random.uniform(70, 100)
            gas = random.uniform(10, 25)
        elif self.scenario == "SMOKE_SPREAD":
            smoke = random.uniform(55, 90)
            temperature = random.uniform(40, 65)
        elif self.scenario == "SENSOR_FAILURE":
            status = "FAULT"
        elif self.scenario == "GATEWAY_FAILURE":
            status = "OFFLINE"
        elif self.scenario == "BLOCKED_EXIT":
            zone = random.choice(["Exit A", "Exit B"])
            status = "DEGRADED"
        elif self.scenario == "MULTI_HAZARD":
            temperature = random.uniform(65, 100)
            smoke = random.uniform(60, 100)
            gas = random.uniform(10, 30)
            occupancy = random.randint(50, 100)
        elif self.scenario == "RECOVERY":
            temperature = random.uniform(22, 28)
            smoke = random.uniform(0, 5)
            gas = random.uniform(0, 2)

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "zone": zone,
            "temperature": round(temperature, 2),
            "smoke": round(smoke, 2),
            "gas": round(gas, 2),
            "occupancy": occupancy,
            "status": status,
            "scenario": self.scenario,
        }

simulator = Simulator()
