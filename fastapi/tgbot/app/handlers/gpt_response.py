import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dependency_injector.wiring import inject, Provide

from core.container import Container
from services.openai_service import OpenAIClient
from utils.const import ERROR_MESSAGE

from core.p_decorator import paycheck

gpt_response = Router()


@gpt_response.message(F.text)
@inject
@paycheck
async def message(
    message: Message,
    state: FSMContext,
    openai_client: OpenAIClient = Provide[Container.openai_client],
) -> None:
    data = await state.get_data()

    if data.get("ready", True):
        await state.update_data(ready=False)

        thread_id = data.get("thread_id", None)
        if not thread_id:
            thread_id = await openai_client.start_threading()
            await state.update_data(thread_id=thread_id)

        await message.bot.send_chat_action(
            chat_id=message.from_user.id, action="typing"
        )

        try:
            answer = await openai_client.get_answer(thread_id, message.text)
            await message.answer(answer)
        except Exception as e:
            await message.answer(ERROR_MESSAGE)
            logging.error(f"Ошибка при обработке сообщения: {e}")

        await state.update_data(ready=True)
    else:
        await message.answer("Пожалуйста, дождитесь ответа от бота")
        await message.bot.send_chat_action(
            chat_id=message.from_user.id, action="typing"
        )
