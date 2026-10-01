import asyncio
from src.core.database import Base, engine
from src import models  # noqa: F401  (нужен, чтобы таблицы попали в Base.metadata)


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())