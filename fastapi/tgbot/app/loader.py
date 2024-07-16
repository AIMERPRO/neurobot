from aiogram import Bot, Dispatcher

from core.config import settings

bot = Bot(settings.bot_token)
dp = Dispatcher()
