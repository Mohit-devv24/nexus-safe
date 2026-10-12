from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from app.core.database import Base

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    building = Column(String(100), default="Main Building")
    floor = Column(String(50), default="Ground Floor")
    zone = Column(String(100), nullable=False)
    value = Column(Float, default=0)
    unit = Column(String(30), default="")
    status = Column(String(30), default="HEALTHY")
    heartbeat = Column(DateTime, default=datetime.utcnow)
    battery = Column(Float, default=100)
    signal = Column(Float, default=100)
    fault = Column(Boolean, default=False)
