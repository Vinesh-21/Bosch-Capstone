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
        func.avg(KPIModel.fuel_per_knot).label("avg_fuel_per_knot"),
        func.avg(KPIModel.fuel_per_torque).label("avg_fuel_per_torque"),
        func.avg(KPIModel.fuel_per_revolution).label("avg_fuel_per_revolution"),
        func.avg(KPIModel.propeller_imbalance).label("avg_propeller_imbalance"),
        func.avg(KPIModel.compressor_temp_ratio).label("avg_compressor_temp_ratio"),
        func.avg(KPIModel.turbine_temp_ratio).label("avg_turbine_temp_ratio"),
        func.avg(KPIModel.compressor_pressure_ratio).label("avg_compressor_pressure_ratio"),
        func.avg(KPIModel.expansion_ratio).label("avg_expansion_ratio"),
        func.avg(KPIModel.torque_per_rpm).label("avg_torque_per_rpm"),
        func.avg(KPIModel.power_per_knot).label("avg_power_per_knot"),
        func.avg(KPIModel.tic_efficiency).label("avg_tic_efficiency"),
        
    )

    result = await session.execute(query)
    avg_data = result.mappings().first()  


    sensor_query = select(Sensor_Readings).order_by(Sensor_Readings.id).limit(1)
    sensor_result = await session.execute(sensor_query)
    first_sensor = sensor_result.scalars().first()

    

    sensor_data = {
            "decay_comp": first_sensor.decay_comp,
            "decay_turbine": first_sensor.decay_turbine
        }
    health = {}
    health.update(avg_data)
    health.update(sensor_data)
    return {
        **health
    }


### Create KPI Value 
@app.post("/add_KPI")
async def KPI_Insertion(
    KPI_List: List[KPISchema],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    KPI_records = [KPIModel(**record.model_dump()) for record in KPI_List]
    
    # Add all records individually
    for record in KPI_records:
        session.add(record)
    
    await session.commit()
    
    return {"inserted": len(KPI_records)}
    
    
### Sensor-Metrics
@app.get("/sensor-metrics/")
async def sensor_metrics(session: Annotated[AsyncSession, Depends(get_session)] ):


    query = (
        select(Sensor_Readings)
        .order_by(Sensor_Readings.time.desc())
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
    return {"status": "Alert created", "alert_id": new_alert.Alert_id}


