from fastapi import FastAPI,Depends
from typing import Annotated
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

@app.get("/add")
async def add(session: Annotated[AsyncSession, Depends(get_session)]):
    new_reading = Sensor_Readings(
        lp=1.2,
        v=3.4,
        GTT=5.6,
        GTn=7.8,
        GGn=9.1,
        Ts=2.3,
        Tp=4.5,
        T48=6.7,
        T1=8.9,
        T2=1.0,
        P48=2.2,
        P1=3.3,
        P2=4.4,
        Pexh=5.5,
        TIC=6.6,
        mf=7.7,
        decay_comp=8.8,
        decay_turbine=9.9
    )

    session.add(new_reading)  
    await session.commit()
    await session.refresh(new_reading)
    
    return {"id": new_reading.id}

    