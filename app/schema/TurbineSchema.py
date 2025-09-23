from pydantic import BaseModel

class TurbineSchema(BaseModel):
    name: str
    location: str
    age: int
