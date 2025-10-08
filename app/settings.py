import logging
import sys

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    test: bool = Field("pytest" in sys.modules, validation_alias="TEST")
    DEBUG: bool = Field(True)

    DB_NAME: str = Field("postgres")
    DB_HOST: str = Field("localhost")
    DB_PORT: str = Field("5432")
    DB_USER: str = Field("postgres")
    DB_PASS: str = Field("postgres")

    ENCRYPT_SECRET_KEY: str

    logger: logging.Logger = logging.getLogger("uvicorn.info")

    @field_validator("DB_NAME", mode="before")
    def set_db_name(cls, db, info):
        if info.data["test"]:
            return "test_" + db
        return db

    model_config = SettingsConfigDict(env_file="conf/.env", env_file_encoding="utf-8")

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
