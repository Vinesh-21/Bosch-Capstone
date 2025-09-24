from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.models.Alerts import Alerts
from app.schema.AlertsSchema import AlertsSchema

router = APIRouter()

@router.post("/anomaly-alerts")
async def create_alert(
    alert: AlertsSchema,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    new_alert = Alerts(**alert.model_dump())
    session.add(new_alert)
    await session.commit()
    await session.refresh(new_alert)
    return {"status": "Alert created", "alert_id": new_alert.Alert_id}