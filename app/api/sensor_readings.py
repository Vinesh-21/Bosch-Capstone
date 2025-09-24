from fastapi import APIRouter, Depends
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import get_session
from app.models.Sensor_Readings import Sensor_Readings
from app.schema.SensorReadingSchema import SensorReadingSchema

router = APIRouter()

@router.post("/add_bulk")
async def add_bulk(sensors: List[SensorReadingSchema], session: Annotated[AsyncSession, Depends(get_session)]):

    sensor_models = [Sensor_Readings(**sensor.model_dump()) for sensor in sensors]
    session.add_all(sensor_models)
    await session.commit()
    for sensor in sensor_models:
        await session.refresh(sensor)
    return {"sensor_reading": sensor_models}

@router.get("/sensor-metrics/")
async def sensor_metrics(session: Annotated[AsyncSession, Depends(get_session)]):

    query = select(Sensor_Readings).order_by(Sensor_Readings.time.desc()).limit(1)
    result = await session.execute(query)
    latest = result.scalars().first()
    if not latest:
        return {"error": "No telemetry found"}
    return latest