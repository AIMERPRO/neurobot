import logging
from time import sleep

import httpx

from openai import OpenAI


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
            self.httpx_client = httpx.Client(proxies=proxies)
        else:
            self.httpx_client = httpx.Client()
        self.client = OpenAI(api_key=api_key, http_client=self.httpx_client)
        self.assistant_id = assistant_id

    def start_threading(self):
        """
        Создает новый поток в OpenAI и возвращает его идентификатор.
        """
        try:
            thread = self.client.beta.threads.create()
            return thread.id
        except Exception as e:
            logging.error(f"Ошибка при создании потока: {e}")

    def get_answer(self, thread_id, message):
        """
        Отправляет сообщение в указанный поток и запускает задачу
        для получения ответа.
        """
        try:
            self.client.beta.threads.messages.create(
                thread_id=thread_id, role="user", content=message
            )
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id, assistant_id=self.assistant_id
            )
            return self.wait_for_completion(thread_id, run)
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения в поток: {e}")

    def wait_for_completion(self, thread_id, run):
        """
        Проверяет статус выполнения задачи.
        """
        try:
            while run.status not in ["completed", "failed", "cancelled"]:
                sleep(0.5)
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id, run_id=run.id
                )
            if run.status == "completed":
                response = self.client.beta.threads.messages.list(
                    thread_id=thread_id
                )
                messages = response.data
                answer = messages[0].content[0].text.value
                return answer
        except Exception as e:
            logging.error(f"Ошибка при генерации ответа: {e}")
