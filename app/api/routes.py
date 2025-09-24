from fastapi import APIRouter
from app.api.alerts import router as AlertRouter
from app.api.kpis import router as KPIRouter
from app.api.sensor_readings import router as SensorReadingRouter

master_route = APIRouter()

master_route.include_router(AlertRouter,tags=["Alerts"])
master_route.include_router(KPIRouter,tags=["KPIs"])
master_route.include_router(SensorReadingRouter,tags=["Sensors"])