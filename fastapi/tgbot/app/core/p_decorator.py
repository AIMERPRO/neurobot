import datetime
import functools

from aiogram.types import Message
from loguru import logger

from database.models import User


def paycheck(func):
    @functools.wraps(func)
    async def wrapped(msg: Message, *args, **kwargs):
        user = await User.query.where(User.chat_id == str(msg.from_user.id)).gino.first()

        if user.subscribe_end:
            if datetime.datetime.now() <= user.subscribe_end:
                original_result = await func(msg, *args, **kwargs)

                return original_result

            else:
                await msg.answer("Ваша подписка закончилась \n"
                                 "Оплатить подписку /pay")

        else:
            await msg.answer("Оплатите подписку /pay")

    return wrapped
