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
async def start_handler(msg: Message,     state: FSMContext,
    openai_client: OpenAIClient = Provide[Container.openai_client],):
    chat_id = msg.from_user.id
    user = await User.query.where(User.chat_id == str(chat_id)).gino.first()
    if user:
        pass
    else:
        await User.create(name=msg.from_user.full_name, username=msg.from_user.username, chat_id=str(chat_id))

    await msg.answer("Оплатите подписку /pay")

