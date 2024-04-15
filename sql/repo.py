from abc import abstractmethod
from typing import Optional, Tuple
from sqlalchemy import Row, Sequence, delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from sql.models import Message, Tag, MessageTag


class Repo:

    @abstractmethod
    async def create(self):
        pass

    @abstractmethod
    async def get(slef):
        pass

    @abstractmethod
    async def delete(slef):
        pass


class MessageRepo(Repo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, message_id: int, tags: list, type_: str) -> Message:
        msg = Message(id=message_id, tags=tags, type_=type_)
        check = await self.get(message_id=message_id)
        if not check:
            self.session.add(msg)
            await self.session.commit()
        return msg

    async def get(self, message_id: int) -> Optional[Message]:
        return await self.session.get(Message, message_id)

    async def delete(self, message_id: int) -> None:
        stmt = delete(Message).where(Message.id == message_id)
        await self.session.execute(stmt)
        await self.session.commit()


class TagRepo(Repo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str) -> Tag:
        tag = Tag(name=name)
        check = await self.get(name=name)
        if not check:
            self.session.add(tag)
            await self.session.commit()
        return tag

    async def get(self, name: str) -> Optional[Tag]:
        return await self.session.get(Message, name)

    async def get_by_id(self, id: int) -> Optional[Tag]:
        stmt = select(Tag).where(Tag.id == id)
        return (await self.session.execute(stmt)).one_or_none()

    async def delete(self, message_id: int) -> None:
        stmt = delete(Message).where(Message.id == message_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_all(self) -> Sequence[Row[Tuple[Tag]]]:
        stmt = select(Tag)
        return (await self.session.execute(stmt)).all()


class MessageTagRepo(Repo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, message_id: int, tag_id: int) -> MessageTag:
        msg_tag = MessageTag(message_id=message_id, tag_id=tag_id)
        check = await self.get(message_id=message_id, tag_id=tag_id)
        if not check:
            self.session.add(msg_tag)
            await self.session.commit()
        return msg_tag

    async def get(self, message_id: int, tag_id: int) -> MessageTag | None:
        stmt = (select(MessageTag).
                where(MessageTag.message_id == message_id,
                      MessageTag.tag_id == tag_id))
        return (await self.session.execute(stmt)).one_or_none()

    async def get_by_tag_id(self,
                            tag_id: int) -> Sequence[Row[Tuple[MessageTag]]]:
        stmt = select(MessageTag).where(MessageTag.tag_id == tag_id)
        return (await self.session.execute(stmt)).all()

    async def delete(self, message_id: int, tag_id: int) -> None:
        stmt = delete(MessageTag).where(MessageTag.message_id == message_id,
                                        MessageTag.tag_id == tag_id)
        await self.session.execute(stmt)
        await self.session.commit()
