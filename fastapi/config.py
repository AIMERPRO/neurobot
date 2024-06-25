from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    DB_LOGIN = os.getenv("DB_LOGIN")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = os.getenv("DATABASE_URL").format(DB_LOGIN, DB_PASSWORD, DB_NAME)
    BOT_TOKEN = os.getenv("BOT_TOKEN")


settings = Settings()
