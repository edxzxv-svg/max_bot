from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class GigaChatSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GIGACHAT_")

    TOKEN: str = ""

    # CLIENT_ID: str = '...'
    # CLIENT_SECRET: str = '...'
    # SCOPE: str = "GIGACHAT_API_PERS"
    # MODEL: str = "GigaChat"
    #
    # TEMPERATURE: float = 0.7
    # MAX_TOKENS: int = 1024
    #
    # # SSL Settings
    # VERIFY_SSL: bool =True


class MaxSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MAX_")
    TOKEN: str = ""
    CLIENT_ID: str = ""


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    DSN: PostgresDsn = PostgresDsn(
        "postgresql+asyncpg://admin:admin@host.docker.internal:10101/max_bot_postgres"
    )
    ECHO_SQL: bool = False
    POOL_SIZE: int = 20
    MAX_OVERFLOW: int = 5


class AppSettings(EnvSettings):
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Chat Settings
    MAX_MESSAGE_LENGTH: int = 4000
    CHAT_HISTORY_LIMIT: int = 10
    RATE_LIMIT_PER_USER: int = 30


class Config(EnvSettings):
    app: AppSettings = AppSettings()
    gigachat: GigaChatSettings = GigaChatSettings()
    max: MaxSettings = MaxSettings()
    postgres: PostgresSettings = PostgresSettings()


settings = Config()
