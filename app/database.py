import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Read database configuration from environment variables
DB_NAME = os.getenv("DB_NAME", "fallback_dbname")
DB_USER = os.getenv("DB_USER", "fallback_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "fallback_password")
DB_HOST = os.getenv("DB_HOST", "fallback_host")
DB_PORT = os.getenv("DB_PORT", "fallback_port")

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
