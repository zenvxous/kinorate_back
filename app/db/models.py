from random import randint
from uuid import UUID as uuid_default

from sqlalchemy import (
    Column,
    DateTime,
    func,
)
from sqlalchemy.orm import DeclarativeBase
from uuid_utils import uuid7


def generate_uuid():
    return uuid_default(str(uuid7()))


class Base(DeclarativeBase):
    created_at = Column(DateTime, server_default=func.now())
