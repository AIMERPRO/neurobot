import secrets
from enum import Enum

from pydantic import PostgresDsn, Field, computed_field
from pydantic_settings import BaseSettings


class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


def field_validator(param, mode):
    pass


class Settings(BaseSettings):
    """Настройки проекта"""

    # region Настройки бота
    bot_token: str = Field(title="Токен бота")
    bot_name: str = Field(title="Имя бота", default=None)
    bot_link: str = Field(title="Ссылка на бота", default="https://t.me/")
    message_per_second: float = Field(title="Кол-во сообщений в секунду", default=1)
    log_level: LogLevel = Field(title="Уровень логирования", default=LogLevel.INFO)
    # endregion

    debug: bool = Field(title="Режим отладки", default=True)
    secret_key: str = Field(
        title="Секретный ключ", default_factory=lambda: secrets.token_hex(16)
    )

    # openai
    assistant_id: str = Field(title="ID асистента")
    openai_api_key: str = Field(title="Ключ OpenAI")
    proxy_url: str = Field(title="Прокси", default=None)

    # database
    DB_LOGIN: str = Field(title="Login SQL")
    DB_PASSWORD: str = Field(title="Password SQL")
    DB_NAME: str = Field(title="Name SQL")
    DATABASE_URL: str = Field(title="URL SQL")

    class Config:
        env_file = ".env"


settings = Settings()
