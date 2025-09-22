from sqlmodel import SQLModel
from datetime import date

class TurbineSchema(SQLModel):
    name: str
    location: str

