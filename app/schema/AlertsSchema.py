from pydantic import BaseModel
from typing import Literal

class AlertsSchema(BaseModel):
    sensor_id: str
    kpi_name: str
    kpi_data: float
    alert_message: Literal[
        "Performance_Anomaly",
        "Equipment_Failure",
        "Maintenance_Required",
        "Overheating",
        "Vibration_Anomaly",
        "Pressure_Anomaly",
        "Flow_Anomaly",
        "Efficiency_Issue",
        "Torque_Stress",
        "Safety_Hazard",
        "Environmental_Anomaly",
        "Sensor_Fault"
    ]
    severity: Literal[
        "INFO",
        "WARNING",
        "CRITICAL",
        "ERROR",
        "ALERT"
    ]
