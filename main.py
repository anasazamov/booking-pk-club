from fastapi import FastAPI
from core.api.v1 import (
    auth, 
    refresh, 
    users, 
    branches, 
    verify,
    balance,
    booking,
    transactions
    )
from core.config import settings

app = FastAPI(
    title="PC-Club Booking",
    docs_url="/docs",
    redoc_url=None,
)

app.include_router(auth.router)
app.include_router(refresh.router)
app.include_router(users.router)
app.include_router(branches.router)
app.include_router(verify.router)
app.include_router(balance.router)
app.include_router(booking.router)
app.include_router(transactions.router)


@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the PC-Club Booking API!"}

