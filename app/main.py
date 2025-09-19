from fastapi import FastAPI,Depends,Body
from typing import Annotated,List,Dict,Any
from contextlib import asynccontextmanager

from app.database.session import ping_db,create_db_tables,get_session

from sqlalchemy.ext.asyncio import AsyncSession


from app.models.Sensor_Readings import Sensor_Readings
from sqlmodel import SQLModel

from app.database.session import engine
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app:FastAPI):
    await ping_db()
    await create_db_tables()
    yield


app = FastAPI(lifespan=lifespan)




@app.get("/")
async def home():
    async with engine.begin() as conn:
        result = await conn.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result.fetchall()]
    return {"tables": tables}

@app.post("/add_bulk")
async def add_bulk(data: Dict[str, Any] = Body(...)):
    """
    Accepts bulk sensor data in dictionary form
    (converted from CSV in Jupyter Notebook).
    """

    return {
        "status": "success",
        "keys": list(data.keys()),
        "records": len(next(iter(data.values()), []))  # number of rows
    }