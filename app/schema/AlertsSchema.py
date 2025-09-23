from pydantic import BaseModel
from typing import Literal
from enum import Enum


class AlertMessageEnum(str, Enum):
    Performance_Anomaly = "Performance_Anomaly"
    Equipment_Failure = "Equipment_Failure"
    Maintenance_Required = "Maintenance_Required"
    Overheating = "Overheating"
    Vibration_Anomaly = "Vibration_Anomaly"
    Pressure_Anomaly = "Pressure_Anomaly"
    Flow_Anomaly = "Flow_Anomaly"
    Efficiency_Issue = "Efficiency_Issue"
    Torque_Stress = "Torque_Stress"
    Safety_Hazard = "Safety_Hazard"
    Environmental_Anomaly = "Environmental_Anomaly"
    Sensor_Fault = "Sensor_Fault"


class SeverityEnum(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    ALERT = "ALERT"


class AlertsSchema(BaseModel):
    sensor_id: str
    kpi_name: str
    kpi_data: float
    alert_message: AlertMessageEnum
    severity: SeverityEnum
