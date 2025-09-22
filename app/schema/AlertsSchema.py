from sqlmodel import SQLModel
from datetime import datetime

class AlertsSchema(SQLModel):
    sensor_id: str

