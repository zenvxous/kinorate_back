from uuid import UUID as uuid_default
from enum import Enum
from sqlalchemy import (
    UUID,
    String,
    Integer,
    Text,
    ARRAY,
)
from sqlalchemy import (
    Column,
    DateTime,
    func,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from uuid_utils import uuid7
from app.utils.common import encrypt_password, decrypt_password


def generate_uuid():
    return uuid_default(str(uuid7()))


class Base(DeclarativeBase):
    created_at = Column(DateTime, server_default=func.now())

class EncryptedField:
    def __init__(self, column_name: str):
        self.column_name = column_name

    def __get__(self, obj, objtype=None) -> str | None:
        if obj is None:
            return None
        raw_value = getattr(obj, f"_{self.column_name}")
        if raw_value is None:
            return None
        return decrypt_password(raw_value)

    def __set__(self, obj, value: str) -> None:
        if value is None or value == "":
            return None
        encrypted = encrypt_password(value)
        setattr(obj, f"_{self.column_name}", encrypted)

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=generate_uuid)
    nickname = Column(String(50), nullable=False)
    email = Column(String(256), nullable=False)
    password = EncryptedField("password")

    recention = relationship("Recention", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(UUID, primary_key=True, default=generate_uuid)
    tmdb_id = Column(Integer, nullable=False)   
    genres = Column(ARRAY(String(25)), nullable=False)

    recention = relationship("Recention", back_populates="movie")

class Recention(Base):
    __tablename__ = "recentions"

    id = Column(UUID, primary_key=True, default=generate_uuid)
    rate = Column(Integer, nullable=False, default=0)
    comment = Column(Text, nullable=True)
    movie_status = Column(String(10), nullable=False)
    
    
    user = relationship("User", back_populates="recention")
    movie = relationship("Movie", back_populates="recention")
