from fastapi import FastAPI,Depends,Body
from typing import Annotated,List,Any
from contextlib import asynccontextmanager

from app.database.session import ping_db,create_db_tables,get_session

### SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

### Request Body Schema
from app.schema.SensorReadingSchema import SensorReadingSchema
from app.schema.AlertsSchema import AlertsSchema
from app.schema.TurbineSchema import TurbineSchema
from app.schema.KPISchema import KPISchema
### Table Models
from app.models.Sensor_Readings import Sensor_Readings
from app.models.Alerts import Alerts
from app.models.Turbine_Metadata import Turbine_Metadata
from app.models.KPI import KPIModel

from app.database.session import engine
from sqlalchemy import text

from app.api.routes import master_route

@asynccontextmanager
async def lifespan(app:FastAPI):
    await ping_db()
    await create_db_tables()
    yield


app = FastAPI(lifespan=lifespan)

### Router
app.include_router(master_route)


@app.get("/")
async def home():
    async with engine.begin() as conn:
        result = await conn.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result.fetchall()]
    return {"tables": tables}