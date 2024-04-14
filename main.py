import asyncio
from aiogram import Bot, Dispatcher
from middlewares.db_middleware import DataBaseMiddelware
from handlers.basic import basic_router
from handlers.tags import tags_router
from sql.db import create_pool
from config import settings

session_factory = create_pool(settings.db_url)


async def main():
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.include_router(basic_router)
    dp.include_router(tags_router)
    dp.update.outer_middleware(DataBaseMiddelware(session_factory))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
