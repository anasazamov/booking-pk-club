from fastapi import FastAPI
from core.api.v1 import auth, users
from core.config import settings

app = FastAPI(
    title="PC-Club Booking",
    docs_url="/docs",
    redoc_url=None,
)

app.include_router(auth.router)
