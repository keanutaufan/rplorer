from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from decouple import config

from app.api.v1.router import api_router

MEDIA_PATH = config("MEDIA_PATH")

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")
app.mount("/uploads", StaticFiles(directory=MEDIA_PATH), name="uploads")