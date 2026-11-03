from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):

    public_bot_token: SecretStr

    postgres_user: SecretStr
    postgres_password: SecretStr
    postgres_host: SecretStr
    postgres_port: int
    postgres_db: SecretStr

    redis_password: SecretStr

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

config = Settings()