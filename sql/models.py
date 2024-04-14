from sqlalchemy import BigInteger, Integer, String, Enum
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            DeclarativeBase)


class Base(DeclarativeBase):
    pass


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    name: Mapped[str] = mapped_column(String)


class MessageTag(Base):
    __tablename__ = "message_tag"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    message_id: Mapped[int] = mapped_column(BigInteger)
    tag_id: Mapped[int] = mapped_column(BigInteger)


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    type_: Mapped[str] = mapped_column(Enum("video", "photo"))
