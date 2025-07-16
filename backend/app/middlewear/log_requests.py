# backend/app/middlewear/log_requests.py

import time

from fastapi import FastAPI, Request

from backend.app.core.logging import api_logger


@app.middlewear("http")
async def log_requests (request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = round(time.time() - start_time, 4)

    api_logger.info(f"{request.method} {request.url.path} - {response.status_code} [{duration}s]")
