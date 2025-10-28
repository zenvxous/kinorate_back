import logging
import sys

from authx import AuthX, AuthXConfig
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

    JWT_SECRET_KEY: str
    JWT_EXPIRY_USER_SECONDS: int = Field(2592000)

    TMDB_API_KEY: str

    logger: logging.Logger = logging.getLogger("uvicorn.info")
    security: AuthX | None = Field(default=None, init=False)

    @field_validator("DB_NAME", mode="before")
    def set_db_name(cls, db, info):
        if info.data["test"]:
            return "test_" + db
        return db

    model_config = SettingsConfigDict(env_file="conf/.env", env_file_encoding="utf-8")

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)

        self.security = AuthX(
            AuthXConfig(
                JWT_ALGORITHM="HS256",
                JWT_SECRET_KEY=self.JWT_SECRET_KEY,
                JWT_TOKEN_LOCATION=["cookies"],
                JWT_ACCESS_COOKIE_NAME="_at",
                JWT_COOKIE_SAMESITE=None,
                JWT_COOKIE_SECURE=False,
                JWT_COOKIE_DOMAIN=None,
            )
        )

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
