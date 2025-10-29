from uuid import UUID as uuid_default

from sqlalchemy import (
    ARRAY,
    UUID,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from uuid_utils import uuid7


def generate_uuid():
    return uuid_default(str(uuid7()))

class Base(DeclarativeBase):
    created_at = Column(DateTime, server_default=func.now())

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=generate_uuid)
    nickname = Column(String(50), nullable=False, unique=True)
    email = Column(String(256), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)

    recention = relationship("Recention", back_populates="user", cascade="all, delete-orphan")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(UUID, primary_key=True, default=generate_uuid)
    tmdb_id = Column(Integer, nullable=False, unique=True, index=True)
    title = Column(String(256), nullable=False)
    genres = Column(ARRAY(String(25)), nullable=False)
    poster_path = Column(String(256), nullable=False)

    recention = relationship("Recention", back_populates="movie", cascade="all, delete-orphan")

class Recention(Base):
    __tablename__ = "recentions"

    id = Column(UUID, primary_key=True, default=generate_uuid)
    rate = Column(Integer, nullable=False, default=0)
    comment = Column(Text, nullable=True)
    movie_status = Column(String(10), nullable=False)

    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(UUID, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="recention")
    movie = relationship("Movie", back_populates="recention")
