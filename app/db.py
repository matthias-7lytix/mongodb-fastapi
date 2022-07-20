from fastapi import FastAPI
import motor.motor_asyncio

from .settings import settings

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient(
    host=settings.mongodb_host,
    port=settings.mongodb_port,
    username=settings.mongodb_user,
    password=settings.mongodb_password,
    authSource="admin",
    uuidRepresentation="standard"
)
db = client["app"]
