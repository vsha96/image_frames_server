# image_frames_server/app/main.py
from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import init_app_db
from .image.router import router as image_router
from .utils.router import router as utils_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_app_db()
    yield
    # Shutdown


app = FastAPI(lifespan=lifespan)


app.include_router(image_router, prefix="/image")
app.include_router(utils_router)
