from fastapi import FastAPI
from app.routes import health, metrics

app = FastAPI(
    title="Server Health Check API",
    description="REST API that exposes server health metrics — CPU, memory, and disk usage.",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(metrics.router)