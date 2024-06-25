import asyncio
import logging
import os
import uuid

from aiogram import Bot, Dispatcher, types, Router
from aiogram.dispatcher import router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from database.connect import connect_db, disconnect_db
from database.models import User, Transaction, Payment, Transaction


load_dotenv()

logging.basicConfig(level=logging.INFO)


router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    chat_id = msg.from_user.id
    user = await User.query.where(User.chat_id == str(chat_id)).gino.first()
    if user:
        pass
    else:
        await User.create(name=msg.from_user.full_name, username=msg.from_user.username, chat_id=str(chat_id))

    await msg.answer("Оплати подписку /pay")


@router.message(Command("pay"))
async def pay_handler(msg: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1 день (300 руб)", callback_data="1_day"),
            InlineKeyboardButton(text="7 дней (1000 руб)", callback_data="7_days"),
            InlineKeyboardButton(text="1 месяц (3000 руб)", callback_data="1_month"),
        ]
    ])
    await msg.answer("Выберите срок подписки: ", reply_markup=markup)


@router.callback_query(lambda c: c.data == '1_day')
async def pay_handler(callback: CallbackQuery):
    user = await User.query.where(User.chat_id == str(callback.from_user.id)).gino.first()

    order_uuid = uuid.uuid4()

    payment = await Payment.create(
        user_id=user.id,
        uuid=str(order_uuid),
        amount=float(300),
        chat_id=str(callback.from_user.id),
        days_of_subscription=1
    )

    link_for_pay = (f"https://payanyway.ru/assistant.htm?MNT_ID=19684417&MNT_AMOUNT=1"
                    f"&MNT_TRANSACTION_ID=sub_{payment.id}_{order_uuid}"
                    f"&MNT_CURRENCY_CODE=RUB&MNT_TEST_MODE=0&MNT_SUBSCRIBER_ID={callback.from_user.id}")

    await payment.update(transaction_id=f"sub_{payment.id}_{order_uuid}").apply()

    await callback.answer(cache_time=30)
    await callback.message.answer(f"Оплатите подписку по <a href='{link_for_pay}'> ССЫЛКЕ </a>", parse_mode="HTML")


@router.callback_query(lambda c: c.data == '7_days')
async def pay_handler(callback: CallbackQuery):
    user = await User.query.where(User.chat_id == str(callback.from_user.id)).gino.first()

    order_uuid = uuid.uuid4()

    payment = await Payment.create(
        user_id=user.id,
        uuid=str(order_uuid),
        amount=float(1000),
        chat_id=str(callback.from_user.id),
        days_of_subscription=7
    )

    link_for_pay = (f"https://payanyway.ru/assistant.htm?MNT_ID=19684417&MNT_AMOUNT=1"
                    f"&MNT_TRANSACTION_ID=sub_{payment.id}_{order_uuid}"
                    f"&MNT_CURRENCY_CODE=RUB&MNT_TEST_MODE=0&MNT_SUBSCRIBER_ID={callback.from_user.id}")

    await payment.update(transaction_id=f"sub_{payment.id}_{order_uuid}").apply()

    await callback.answer(cache_time=30)
    await callback.message.answer(f"Оплатите подписку по <a href='{link_for_pay}'> ССЫЛКЕ </a>", parse_mode="HTML")


@router.callback_query(lambda c: c.data == '1_month')
async def pay_handler(callback: CallbackQuery):
    user = await User.query.where(User.chat_id == str(callback.from_user.id)).gino.first()

    order_uuid = uuid.uuid4()

    payment = await Payment.create(
        user_id=user.id,
        uuid=str(order_uuid),
        amount=float(3000),
        chat_id=str(callback.from_user.id),
        days_of_subscription=30
    )

    link_for_pay = (f"https://payanyway.ru/assistant.htm?MNT_ID=19684417&MNT_AMOUNT=1"
                    f"&MNT_TRANSACTION_ID=sub_{payment.id}_{order_uuid}"
                    f"&MNT_CURRENCY_CODE=RUB&MNT_TEST_MODE=0&MNT_SUBSCRIBER_ID={callback.from_user.id}")

    await payment.update(transaction_id=f"sub_{payment.id}_{order_uuid}").apply()

    await callback.answer(cache_time=30)
    await callback.message.answer(f"Оплатите подписку по <a href='{link_for_pay}'> ССЫЛКЕ </a>", parse_mode="HTML")


async def on_startup():
    await connect_db()


async def on_shutdown():
    await disconnect_db()


async def main():
    await on_startup()  # Подключаемся к базе данных
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    await on_shutdown()  # Отключаемся от базы данных


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())