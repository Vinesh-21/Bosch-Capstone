from sqlmodel import SQLModel, Field
from uuid import uuid4

class KPIModel(SQLModel, table=True):
    __tablename__ = "kpi"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    
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
