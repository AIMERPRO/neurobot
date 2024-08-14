from aiogram import Router

from .start import start_router
from .gpt_response import gpt_response
from .subscription import subs_router


def get_all_routers() -> Router:
    """Функция для регистрации всех router"""

    router = Router()
    router.include_router(start_router)
    router.include_router(subs_router)
    router.include_router(gpt_response)

    return router
