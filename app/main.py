from fastapi import FastAPI

from app.api.v1.router import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")