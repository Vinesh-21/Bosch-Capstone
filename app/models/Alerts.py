from sqlmodel import SQLModel, Field
from uuid import uuid4
from enum import Enum
class AlertType(str, Enum):
    performance = "Performance_Anomaly"
    equipment = "Equipment_Failure"
    maintenance = "Maintenance_Required"
    overheating = "Overheating"
    vibration = "Vibration_Anomaly"
    pressure = "Pressure_Anomaly"
    flow = "Flow_Anomaly"
    efficiency = "Efficiency_Issue"
    torque = "Torque_Stress"
    safety = "Safety_Hazard"
    environmental = "Environmental_Anomaly"
    sensor = "Sensor_Fault"


class Severity(str, Enum):
    info = "INFO"
    warning = "WARNING"
    critical = "CRITICAL"
    error = "ERROR"
    alert = "ALERT"


class Alerts(SQLModel, table=True):
    __tablename__ = "alerts"

    Alert_id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    sensor_id: str = Field(foreign_key="sensor_readings.id")
    kpi_name:str
    kpi_data:float
    alert_message:AlertType
    severity:Severity