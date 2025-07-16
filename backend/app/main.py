# /backend/app/main.py

from fastapi import FastAPI

from backend.app.api.v1 import api_router

app = FastAPI(title="cve2cli API")

app.include_router(api_router, prefix="/api/v1")
