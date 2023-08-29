from fastapi import FastAPI

from .router.health import health_v1

app = FastAPI()

app.include_router(health_v1)
