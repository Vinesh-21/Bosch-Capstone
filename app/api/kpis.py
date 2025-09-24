from fastapi import APIRouter, Depends
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database.session import get_session
from app.models.KPI import KPIModel
from app.models.Sensor_Readings import Sensor_Readings
from app.schema.KPISchema import KPISchema

router = APIRouter()

@router.get("/health-summary")
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
    
    return {
        "KPI_Metrics":avg_data,
        "decay_status":sensor_data
    }


@router.post("/add_KPI")
async def kpi_insertion(
    kpi_list: List[KPISchema],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    
    kpi_records = [KPIModel(**record.model_dump()) for record in kpi_list]
    for record in kpi_records:
        session.add(record)
    await session.commit()
    return {"KPI_Records": [record.model_dump() for record in kpi_records]}