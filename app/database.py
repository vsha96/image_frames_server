# image_frames_server/app/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Import CSV image data after initializing the database
    from app.image.utils import import_csv_to_db

    await import_csv_to_db("app/image/data/img.csv")


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
