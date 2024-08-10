import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.core.configs import settings
from app.core.database import engine


async def create_tables() -> None:
    import models.__all_models
    async with engine.begin() as conn:
        await conn.run_sync(settings.DB_BASE_URL.metadata.drop_all)
        await conn.run_sync(settings.DB_BASE_URL.metadata.create_all)


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())
