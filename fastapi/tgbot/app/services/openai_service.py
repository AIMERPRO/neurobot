import asyncio
import logging

import httpx

from utils.const import ERROR_MESSAGE
from openai import AsyncOpenAI


class OpenAIClient:
    """
    Клиент для работы с OpenAI API, предоставляющий функции для
    создания потоков, отправки сообщений и управления выполнением задач.
    """

    def __init__(self, api_key, assistant_id, proxy_url=None):
        if proxy_url:
            proxies = {
                "http://": proxy_url,
                "https://": proxy_url,
            }
            self.httpx_client = httpx.AsyncClient(proxies=proxies)
        else:
            self.httpx_client = httpx.AsyncClient()
        self.client = AsyncOpenAI(api_key=api_key, http_client=self.httpx_client)
        self.assistant_id = assistant_id

    async def start_threading(self):
        """
        Создает новый поток в OpenAI и возвращает его идентификатор.
        """
        try:
            thread = await self.client.beta.threads.create()
            return thread.id
        except Exception as e:
            logging.error(f"Ошибка при создании потока: {e}")
            return None

    async def get_answer(self, thread_id, message):
        """
        Отправляет сообщение в указанный поток и запускает задачу
        для получения ответа.
        """
        try:
            await self.client.beta.threads.messages.create(
                thread_id=thread_id, role="user", content=message
            )
            run = await self.client.beta.threads.runs.create(
                thread_id=thread_id, assistant_id=self.assistant_id
            )
            return await self.wait_for_completion(thread_id, run)
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения в поток: {e}")
            return ERROR_MESSAGE

    async def wait_for_completion(self, thread_id, run):
        """
        Проверяет статус выполнения задачи.
        """
        try:
            while run.status not in ["completed", "failed", "cancelled"]:
                await asyncio.sleep(0.5)
                run = await self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id, run_id=run.id
                )
            if run.status == "completed":
                response = await self.client.beta.threads.messages.list(
                    thread_id=thread_id
                )
                messages = response.data
                answer = messages[0].content[0].text.value
                return answer
            else:
                return ERROR_MESSAGE
        except Exception as e:
            logging.error(f"Ошибка при генерации ответа: {e}")
            return ERROR_MESSAGE
