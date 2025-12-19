from fastapi import FastAPI
from gitfastapi.api.endpoints import router

app = FastAPI()

app.include_router(router)