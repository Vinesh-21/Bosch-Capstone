#Session.py
from app.models.Sensor_Readings import Sensor_Readings

from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm.session import sessionmaker

from app.config import databaseSettings

from sqlalchemy import text

from sqlmodel import SQLModel



engine = create_async_engine(
    url=databaseSettings.get_MYSQL_URL,
    echo=True
)


async def create_db_tables():
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Tables created.")

async def ping_db():
    async with engine.begin() as conn:
        try:

            await conn.execute(text("SHOW Tables"))
            print("Successful Connected to DB ")
        except Exception as e:
            print("Unsuccessful Database Connection due to: ",e)





async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session():
    async with async_session() as session:
        yield session