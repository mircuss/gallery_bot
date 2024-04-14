from abc import abstractmethod
from typing import Optional
from sqlalchemy import delete
from sqlalchemy.ext.asyncio.session import AsyncSession

from sql.models import Message, Tag


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
        msg = Message(id=message_id, tags=tags, type=type_)
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

    async def delete(self, message_id: int) -> None:
        stmt = delete(Message).where(Message.id == message_id)
        await self.session.execute(stmt)
        await self.session.commit()
