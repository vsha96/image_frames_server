import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Define constants for database configuration
DB_NAME = "dbname"
DB_USER = "user"
DB_PASSWORD = "password"
DB_HOST = "db"
DB_PORT = "5432"

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def init_app_db():
    await drop_tables()
    await create_tables()

    if os.environ.get("TESTING") == "True":
        return

    # Import CSV image data after initializing the database
    from app.image.utils import import_csv_to_db

    await import_csv_to_db("app/image/data/img.csv")


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
