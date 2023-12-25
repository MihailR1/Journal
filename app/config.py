import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LOG_LEVEL: str = 'INFO'
    BASEDIR: str = os.path.abspath(os.path.dirname(__file__))
    ENV_FILE_PATH: str = os.path.join(BASEDIR, '..', '.env')

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    DB_ENGINE: str = 'asyncpg'
    DB_TYPE: str = 'postgresql'

    @property
    def DATABASE_URL(self) -> str:
        return f'{self.DB_TYPE}+{self.DB_ENGINE}://{self.DB_LOGIN}:' \
               f'{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra='ignore')


settings = Settings()
