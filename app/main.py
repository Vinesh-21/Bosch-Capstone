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

### Table Models
from app.models.Sensor_Readings import Sensor_Readings
from app.models.Alerts import Alerts
from app.models.Turbine_Metadata import Turbine_Metadata


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
async def add_bulk(sensors:List[SensorReadingSchema],session:Annotated[AsyncSession,Depends(get_session)]):
    sensor_models = [Sensor_Readings(**sensor.dict()) for sensor in sensors]

    session.add_all(sensor_models)
    await session.commit()
    
    for sensor in sensor_models:
        await session.refresh(sensor)

    return {"inserted": len(sensor_models)}
    

### Health-Summary
@app.get("/health-summary")
async def health_summary(session: Annotated[AsyncSession, Depends(get_session)]):
    query = select(
        func.sum(Sensor_Readings.mf).label("total_fuel"),
        func.avg(Sensor_Readings.decay_comp).label("avg_decay_comp"),
        func.avg(Sensor_Readings.decay_turbine).label("avg_decay_turbine")
    )
    result = await session.execute(query)
    summary = result.mappings().first()
    return summary


### Sensor-Metrics
@app.get("/sensor-metrics/")
async def sensor_metrics(session: Annotated[AsyncSession, Depends(get_session)] ):


    query = (
        select(Sensor_Readings)
        .order_by(Sensor_Readings.id.desc())
        .limit(1)
    )
    result = await session.execute(query)
    latest = result.scalars().first()
    if not latest:
        return {"error": "No telemetry found"}
    return latest.model_dump()


### ALERTS 
@app.post("/anomaly-alerts")
async def create_alert(
    alert: AlertsSchema,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    new_alert = Alerts(**alert.model_dump())
    session.add(new_alert)
    await session.commit()
    await session.refresh(new_alert)
    return {"status": "Alert created", "alert_id": new_alert.id}


# from fastapi import FastAPI, UploadFile, File

# @app.post("/upload")
# async def fileUpload(file: UploadFile = File(...)):
#     return {
#         "filename": file.filename,
#         "content_type": file.content_type,
#         "file_size": len(await file.read()) 
#     }


from fastapi import HTTPException,status


# @app.post("/auth")
# def auth(token: str):
#     if token == "vinesh":
#         return HTTPException(
#             status_code=status.HTTP_200_OK,detail={
#             "Auth":"Authorized"
#         })
#     return HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail={"message":"Invalid Token"})