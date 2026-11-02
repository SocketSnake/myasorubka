from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):

    mmyaso_tg_bot_token: SecretStr

    superuser_tg_id: int

    db_login: SecretStr
    db_password: SecretStr

    redis_password: SecretStr

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

config = Settings()