from typing import List
from sqlalchemy import BigInteger, String, Enum
from sqlalchemy.orm import (Mapped, relationship,
                            mapped_column,
                            DeclarativeBase)


class Base(DeclarativeBase):
    pass


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String)


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    types: Mapped[str] = mapped_column(Enum("video", "photo"))
    tags: Mapped[List["Tag"]] = relationship()
