FROM python:3.9-slim

WORKDIR /bot

COPY tgbot/requirements.txt .
COPY database tgbot/app/database
COPY config.py tgbot/app/config.py
COPY .env tgbot/app/.env

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "tgbot/app/main.py"]
