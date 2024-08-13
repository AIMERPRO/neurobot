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


@start_router.message(Command("pay"))
async def pay_handler(msg: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1 день (300 руб)", callback_data="1_day"),
            InlineKeyboardButton(text="7 дней (1000 руб)", callback_data="7_days"),
            InlineKeyboardButton(text="1 месяц (3000 руб)", callback_data="1_month"),
        ]
    ])
    await msg.answer("Выберите срок подписки: ", reply_markup=markup)


@start_router.callback_query(lambda c: c.data == '1_day')
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


@start_router.callback_query(lambda c: c.data == '7_days')
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

    link_for_pay = (f"https://payanyway.ru/assistant.htm?MNT_ID=19684417&MNT_AMOUNT=2"
                    f"&MNT_TRANSACTION_ID=sub_{payment.id}_{order_uuid}"
                    f"&MNT_CURRENCY_CODE=RUB&MNT_TEST_MODE=0&MNT_SUBSCRIBER_ID={callback.from_user.id}")

    await payment.update(transaction_id=f"sub_{payment.id}_{order_uuid}").apply()

    await callback.answer(cache_time=30)
    await callback.message.answer(f"Оплатите подписку по <a href='{link_for_pay}'> ССЫЛКЕ </a>", parse_mode="HTML")


@start_router.callback_query(lambda c: c.data == '1_month')
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

    link_for_pay = (f"https://payanyway.ru/assistant.htm?MNT_ID=19684417&MNT_AMOUNT=3"
                    f"&MNT_TRANSACTION_ID=sub_{order_uuid}"
                    f"&MNT_CURRENCY_CODE=RUB&MNT_TEST_MODE=0&MNT_SUBSCRIBER_ID={callback.from_user.id}")

    await payment.update(transaction_id=f"sub_{payment.id}_{order_uuid}").apply()

    await callback.answer(cache_time=30)
    await callback.message.answer(f"Оплатите подписку по <a href='{link_for_pay}'> ССЫЛКЕ </a>", parse_mode="HTML")


