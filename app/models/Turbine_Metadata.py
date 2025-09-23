from sqlmodel import SQLModel, Field
from uuid import uuid4

class Turbine_Metadata(SQLModel, table=True):
    __tablename__ = "turbine_metadata"

    turbine_id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    location: str
    age:int

