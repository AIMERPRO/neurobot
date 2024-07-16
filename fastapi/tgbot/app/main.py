import asyncio

from loguru import logger

from handlers.routing import get_all_routers

from middlewares.throttling import rate_limit_middleware

from core.container import Container
import handlers

from database.connect import connect_db, disconnect_db
from loader import dp, bot


async def on_startup():
    await connect_db()


async def on_shutdown():
    await disconnect_db()


async def main(container: Container):
    """Запуск бота."""
    try:
        # sync_session = container.session()
        await on_startup()  # Подключаемся к базе данных
        all_routers = get_all_routers()
        dp.include_routers(all_routers)
        dp.message.middleware(rate_limit_middleware)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await on_shutdown()  # Отключаемся от базы данных


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[handlers])
    logger.info("Bot is starting")
    asyncio.run(main(container=container))
