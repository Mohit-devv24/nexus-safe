from datetime import datetime
from pydantic import BaseModel

class SensorResponse(BaseModel):
    id: int
    sensor_id: str
    name: str
    category: str
    building: str
    floor: str
    zone: str
    value: float
    unit: str
    status: str
    heartbeat: datetime
    battery: float
    signal: float
    fault: bool

    class Config:
        from_attributes = True
