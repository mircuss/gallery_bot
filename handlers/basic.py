import asyncio
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from sql.repo import TagRepo, MessageTagRepo
from keyboards.inline import generate_tag_keyboard

from config import settings

basic_router = Router()


@basic_router.message(F.photo)
async def photo(message: Message, tag: TagRepo):
    tags = await tag.get_all()
    markup = generate_tag_keyboard(tags=tags[:10], last=10)
    await message.send_copy(chat_id=message.chat.id, reply_markup=markup)
    await message.send_copy(chat_id=settings.channel_id, reply_markup=markup)


@basic_router.message(F.video)
async def video(message: Message, tag: TagRepo):
    tags = await tag.get_all()
    markup = generate_tag_keyboard(tags=tags[:10], last=10)
    await message.send_copy(chat_id=message.chat.id, reply_markup=markup)
    await message.send_copy(chat_id=settings.channel_id, reply_markup=markup)


@basic_router.callback_query(F.data.startswith("tag_"))
async def tag(call: CallbackQuery, tag: TagRepo, tag_message: MessageTagRepo):
    await call.answer()
    tag_id = call.data.split("_")[1]
    tag_name = (await tag.get_by_id(id=tag_id))[0]
    tag = await tag_message.get(message_id=call.message.message_id,
                                tag_id=tag_id)
    if tag:
        await tag_message.delete(message_id=call.message.message_id,
                                 tag_id=tag_id)
        msg = await call.message.answer(text=f" REMOVE {tag_name.name}")
        await asyncio.sleep(10)
        await msg.delete()
        return
    await tag_message.create(message_id=call.message.message_id, tag_id=tag_id)
    msg = await call.message.answer(text=f" ADD {tag_name.name}")
    await asyncio.sleep(10)
    await msg.delete()


@basic_router.callback_query(F.data.startswith("prev_"))
async def prev(call: CallbackQuery, tag: TagRepo):
    await call.answer()
    last = int(call.data.split("_")[1])
    if last == 10:
        return
    tags = await tag.get_all()
    markup = generate_tag_keyboard(tags=tags[last-20:last-10], last=last-10)
    await call.message.edit_reply_markup(reply_markup=markup)


@basic_router.callback_query(F.data.startswith("next_"))
async def next(call: CallbackQuery, tag: TagRepo):
    await call.answer()
    tags = await tag.get_all()
    last = int(call.data.split("_")[1])
    if last >= len(tags):
        return
    markup = generate_tag_keyboard(tags=tags[last:last+10], last=last+10)
    await call.message.edit_reply_markup(reply_markup=markup)
