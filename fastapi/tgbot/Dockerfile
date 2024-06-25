FROM python:3.9-slim

WORKDIR /app

COPY tgbot/requirements.txt .
COPY database tgbot/database
COPY config.py tgbot/config.py
COPY .env tgbot/.env

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "tgbot/aiogram_bot.py"]
