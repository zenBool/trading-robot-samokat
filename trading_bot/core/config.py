from pathlib import Path
from typing import Optional, Tuple, Type

from pydantic import BaseModel
from pydantic import PostgresDsn

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
)


BASE_DIR = Path(__file__).parent.parent

# CRITICAL = 50
# FATAL = CRITICAL
# ERROR = 40
# WARNING = 30
# WARN = WARNING
# INFO = 20
# DEBUG = 10
# NOTSET = 0
LOG_LEVEL: str = "DEBUG"


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000


class APIPrefix_v1(BaseModel):
    prefix: str = "/v1"
    tag: str = "API_v1"
    account: str = "/account"
    trade: str = "/trade"
    users: str = "/users"


class APIPrefix(BaseModel):
    prefix: str = "/api"
    tag: str = "API"
    v1: APIPrefix_v1 = APIPrefix_v1()


class DBConfig(BaseModel):
    url: Optional[PostgresDsn] = (
        "postgresql+asyncpg://postgres:@192.168.3.50:5432/autotrader"
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
        env_prefix="FRONT__",
        extra="ignore",
    )
    run: RunConfig = RunConfig()
    api: APIPrefix = APIPrefix()
    db: DBConfig = DBConfig()
    log_level: str = LOG_LEVEL
    log_dir: Path = BASE_DIR / "logs"

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
    pass
