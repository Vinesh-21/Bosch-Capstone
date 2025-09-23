from pydantic import BaseModel
from typing import List

class SensorReadingSchema(BaseModel):
    lp: float
    v: float
    GTT: float
    GTn: float
    GGn: float
    Ts: float
    Tp: float
    T48: float
    T1: float
    T2: float
    P48: float
    P1: float
    P2: float
    Pexh: float
    TIC: float
    mf: float
    decay_comp: float
    decay_turbine: float
    time:int