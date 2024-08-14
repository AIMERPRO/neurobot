import datetime
import uuid

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart, Command

from dependency_injector.wiring import inject, Provide

from core.container import Container
from services.openai_service import OpenAIClient

from database.models import User, Payment

from core.p_decorator import paycheck

from loguru import logger

start_router = Router()



@start_router.message(Command("start"))
@inject
async def start_handler(msg: Message):
    user = await User.query.where(User.chat_id == str(msg.from_user.id)).gino.first()

    if user.subscribe_end <= datetime.datetime.now():
        chat_id = msg.from_user.id
        user = await User.query.where(User.chat_id == str(chat_id)).gino.first()
        if user:
            pass
        else:
            await User.create(name=msg.from_user.full_name, username=msg.from_user.username, chat_id=str(chat_id))

        await msg.answer("Оплатите подписку /pay")

    else:
        await msg.answer(f"Ваша подписка оплачена до {datetime.datetime.strftime(user.subscribe_end, "%d-%m-%Y, %H-%S")}")
