# app/api/v1/__init__.py

from fastapi import APIRouter

from .vendors import router as vendor_router

api_router = APIRouter()
api_router.include_router(vendor_router)
