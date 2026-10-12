from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.core.database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(100), nullable=False)
    severity = Column(String(30), default="MEDIUM")
    zone = Column(String(100), nullable=False)
    state = Column(String(50), default="NEW")
    title = Column(String(250), nullable=False)
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
