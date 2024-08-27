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

from core.config import settings

from loguru import logger

subs_router = Router()


@subs_router.message(Command("pay"))
async def pay_handler(msg: Message):
    user = await User.query.where(User.chat_id == str(msg.from_user.id)).gino.first()

    if user.subscribe_end:
        if user.subscribe_end <= datetime.datetime.now():

            markup = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="1 день (300 руб)", callback_data="1_day"),
                    InlineKeyboardButton(text="7 дней (1000 руб)", callback_data="7_days"),
                    InlineKeyboardButton(text="1 месяц (3000 руб)", callback_data="1_month"),
                ]
            ])
            await msg.answer("Выберите срок подписки: ", reply_markup=markup)

        else:
            await msg.answer(f'У вас уже есть подписка до: {datetime.datetime.strftime(user.subscribe_end, "%d-%m-%Y, %H-%M")}')

    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="1 день (300 руб)", callback_data="1_day"),
                InlineKeyboardButton(text="7 дней (1000 руб)", callback_data="7_days"),
                InlineKeyboardButton(text="1 месяц (3000 руб)", callback_data="1_month"),
            ]
        ])
        await msg.answer("Выберите срок подписки: ", reply_markup=markup)


@subs_router.callback_query(lambda c: c.data == '1_day')
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

    link_for_pay = (f"https://payanyway.ru/assistant.htm?MNT_ID=19684417&MNT_AMOUNT={settings.oneday_subs}"
                    f"&MNT_TRANSACTION_ID=sub_{payment.id}_{order_uuid}"
                    f"&MNT_CURRENCY_CODE=RUB&MNT_TEST_MODE=0&MNT_SUBSCRIBER_ID={callback.from_user.id}")

    await payment.update(transaction_id=f"sub_{payment.id}_{order_uuid}").apply()

    await callback.answer(cache_time=30)
    await callback.message.answer(f"Оплатите подписку по <a href='{link_for_pay}'> ССЫЛКЕ </a>", parse_mode="HTML")


@subs_router.callback_query(lambda c: c.data == '7_days')
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

    link_for_pay = (f"https://payanyway.ru/assistant.htm?MNT_ID=19684417&MNT_AMOUNT={settings.sevenday_subs}"
                    f"&MNT_TRANSACTION_ID=sub_{payment.id}_{order_uuid}"
                    f"&MNT_CURRENCY_CODE=RUB&MNT_TEST_MODE=0&MNT_SUBSCRIBER_ID={callback.from_user.id}")

    await payment.update(transaction_id=f"sub_{payment.id}_{order_uuid}").apply()

    await callback.answer(cache_time=30)
    await callback.message.answer(f"Оплатите подписку по <a href='{link_for_pay}'> ССЫЛКЕ </a>", parse_mode="HTML")


@subs_router.callback_query(lambda c: c.data == '1_month')
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

    link_for_pay = (f"https://payanyway.ru/assistant.htm?MNT_ID=19684417&MNT_AMOUNT={settings.month_subs}"
                    f"&MNT_TRANSACTION_ID=sub_{payment.id}_{order_uuid}"
                    f"&MNT_CURRENCY_CODE=RUB&MNT_TEST_MODE=0&MNT_SUBSCRIBER_ID={callback.from_user.id}")

    await payment.update(transaction_id=f"sub_{payment.id}_{order_uuid}").apply()

    await callback.answer(cache_time=30)
    await callback.message.answer(f"Оплатите подписку по <a href='{link_for_pay}'> ССЫЛКЕ </a>", parse_mode="HTML")


