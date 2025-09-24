import pytest_asyncio  
from httpx import ASGITransport, AsyncClient
from app.main import app

@pytest_asyncio.fixture(scope="session")
async def client():

    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test"
    ) as client:
        yield client