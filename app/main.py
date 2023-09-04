from fastapi import FastAPI

from .router.router import rtr
from .service import strategies

app = FastAPI()

app.include_router(rtr)
