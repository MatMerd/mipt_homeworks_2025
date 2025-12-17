import logging
import sys

from fastapi import FastAPI
from api import router


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(message)s',
    datefmt='%H:%M:%S',
    stream=sys.stdout
)


app = FastAPI()
app.include_router(router, prefix="/repositories")


@app.get("/")
def get() -> str:
    return "Hello!"
