import logging
import time

import psutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import ping, modules_api
from .config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Iamge - Studio",
    description="Image - studio Backend v1",
)

app.include_router(ping.router)
app.include_router(modules_api.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def log_stats(start_time, request):
    end_time = time.time()
    elapsed_time = end_time - start_time

    process = psutil.Process()
    memory_usage = process.memory_info().rss
    cpu_usage = process.cpu_percent()

    print(f"Memory Usage: {memory_usage / 1024 / 1024:.2f} MB")
    print(f"CPU Usage: {cpu_usage}%")
    print(f"Elapsed Time: {elapsed_time:.4f} seconds")


@app.middleware("http")
async def log_request_stats(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    log_stats(start_time, request)
    return response
