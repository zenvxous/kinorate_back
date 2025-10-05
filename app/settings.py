import hashlib
import logging
import sys

from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
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
    fernet: Fernet | None = Field(default=None, init=False)

    @field_validator("DB_NAME", mode="before")
    def set_db_name(cls, db, info):
        if info.data["test"]:
            return "test_" + db
        return db

    model_config = SettingsConfigDict(env_file="conf/.env", env_file_encoding="utf-8")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        key_bytes = hashlib.sha256(self.ENCRYPT_SECRET_KEY.encode("utf-8")).digest()  # 32 байта
        key_b64 = urlsafe_b64encode(key_bytes).decode("utf-8")  # base64
        self.fernet = Fernet(key_b64)

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
