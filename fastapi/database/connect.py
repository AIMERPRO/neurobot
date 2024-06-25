from gino import Gino
from config import settings

db = Gino()


async def connect_db():
    await db.set_bind(settings.DATABASE_URL)


async def disconnect_db():
    await db.pop_bind().close()