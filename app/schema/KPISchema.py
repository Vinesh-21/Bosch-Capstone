from pydantic import BaseModel
from datetime import datetime

class KPISchema(BaseModel):
    fuel_per_knot: float
    fuel_per_torque: float
    fuel_per_revolution: float
    propeller_imbalance: float
    compressor_temp_ratio: float
    turbine_temp_ratio: float
    compressor_pressure_ratio: float
    expansion_ratio: float
    torque_per_rpm: float
    power_per_knot: float
    tic_efficiency: float
