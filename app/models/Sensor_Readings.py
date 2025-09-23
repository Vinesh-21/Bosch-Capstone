from sqlmodel import Field,Column, SQLModel,Relationship
from uuid import uuid4

class Sensor_Readings(SQLModel,table=True):
    __tablename__ = "sensor_readings"
    
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)

    lp: float = Field(nullable=False)
    v: float = Field(nullable=False)
    GTT: float = Field(nullable=False)
    GTn: float = Field(nullable=False)
    GGn: float = Field(nullable=False)
    Ts: float = Field(nullable=False)
    Tp: float = Field(nullable=False)
    T48: float = Field(nullable=False)
    T1: float = Field(nullable=False)
    T2: float = Field(nullable=False)
    P48: float = Field(nullable=False)
    P1: float = Field(nullable=False)
    P2: float = Field(nullable=False)
    Pexh: float = Field(nullable=False)
    TIC: float = Field(nullable=False)
    mf: float = Field(nullable=False)
    decay_comp: float = Field(nullable=False)
    decay_turbine: float = Field(nullable=False)
    time:int