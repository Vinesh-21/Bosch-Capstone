from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import datetime,timezone

class Alerts(SQLModel, table=True):
    __tablename__ = "alerts"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    sensor_id: str = Field(foreign_key="sensor_readings.id")
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc), nullable=False)
