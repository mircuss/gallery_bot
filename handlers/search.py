from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery

from sql.repo import TagRepo, MessageTagRepo
from keyboards.inline import generate_tag_keyboard

from config import settings

search_router = Router()


@search_router.message(F.text == "/search")
async def search(message: Message, tag: TagRepo):
    tags = await tag.get_all()
    markup = generate_tag_keyboard(tags=tags[:10], last=10,
                                   pre="search_", message_id=1)
    await message.send_copy(chat_id=message.chat.id, reply_markup=markup)


@search_router.callback_query(F.data.startswith("search_"))
async def search_tag(call: Message, bot: Bot, tag_message: MessageTagRepo):
    await call.answer()
    tag_id = call.data.split("_")[2]
    msgs = await tag_message.get_by_tag_id(tag_id=tag_id)
    for msg in msgs:
        print(msg[0].message_id)
        await bot.copy_message(from_chat_id=settings.channel_id,
                               message_id=msg[0].message_id,
                               chat_id=call.message.chat.id)


@search_router.callback_query(F.data.startswith("search_prev_"))
async def prev(call: CallbackQuery, tag: TagRepo):
    await call.answer()
    last = int(call.data.split("_")[2])
    if last == 10:
        return
    tags = await tag.get_all()
    markup = generate_tag_keyboard(tags=tags[last-20:last-10], last=last-10)
    await call.message.edit_reply_markup(reply_markup=markup)


@search_router.callback_query(F.data.startswith("search_next_"))
async def next(call: CallbackQuery, tag: TagRepo):
    await call.answer()
    tags = await tag.get_all()
    last = int(call.data.split("_")[2])
    if last >= len(tags):
        return
    markup = generate_tag_keyboard(tags=tags[last:last+10], last=last+10)
    await call.message.edit_reply_markup(reply_markup=markup)
