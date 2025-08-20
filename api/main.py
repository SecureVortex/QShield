from fastapi import FastAPI
from . import routes

app = FastAPI(title="QShield API")

app.include_router(routes.router)
