import motor.motor_asyncio

from .settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(
    settings.mongodb_url,
    authSource="admin",
    uuidRepresentation="standard"
)

db = client["app"]
