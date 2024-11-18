import logging
import os
from pathlib import Path
from typing import Optional, Tuple, Type

from pydantic import BaseModel, model_validator
from pydantic import PostgresDsn

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
)


ENV_DIR = Path(__file__).parents[3]
TEMPLATE_ENV = ENV_DIR / "template.env"
BASE_ENV = ENV_DIR / ".env"


class LogLevel(BaseModel):
    # CRITICAL = 50
    # FATAL = CRITICAL
    # ERROR = 40
    # WARNING = 30
    # WARN = WARNING
    # INFO = 20
    # DEBUG = 10
    # NOTSET = 0
    level: str = "ERROR"

    def get_level(self) -> int:
        return logging.getLevelName(self.level.upper())


class RabbitMQSettings(BaseModel):
    host: str = "rabbitmq"


class BinanceKeys(BaseModel):
    api_key: str = ""
    api_secret: str = ""


class DBBinanceConfig(BaseModel):
    url: Optional[PostgresDsn] = (
        "postgresql+asyncpg://postgres:@192.168.3.50:5432/binance"
    )

    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 45
    pool_size: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../template.env", "../.env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="TRADER__",
    )
    db_binance: DBBinanceConfig = DBBinanceConfig()
    binance: BinanceKeys = BinanceKeys()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    log_level: LogLevel = LogLevel()

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
        **kwargs
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        # Переопределяем порядок источников: переменные окружения имеют высший приоритет
        return env_settings, dotenv_settings, init_settings, file_secret_settings


settings = Settings()


if __name__ == "__main__":
    # print(ENV_DIR, Path.is_file(TEMPLATE_ENV))
    pass
