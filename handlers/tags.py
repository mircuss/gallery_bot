from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from states.tag_states import TagStates
from sql.repo import TagRepo

tags_router = Router()


@tags_router.message(F.text == "/add")
async def get_tag_to_add(message: Message, state: FSMContext):
    await state.set_state(TagStates.add_tag)
    await message.answer("Введите название тега")


@tags_router.message(F.text == "/delete")
async def get_tag_to_delete(message: Message, state: FSMContext):
    await state.set_state(TagStates.delete_tag)
    await message.answer("Введите название тега")


@tags_router.message(StateFilter(TagStates.add_tag))
async def add_tag(message: Message, state: FSMContext, tag: TagRepo):
    await tag.create(name=message.text)
    await message.answer("Тег успешно добавлен")
    await state.clear()


@tags_router.message(StateFilter(TagStates.delete_tag))
async def delete_tag(message: Message, state: FSMContext, tag: TagRepo):
    await tag.delete(name=message.text)
    await message.answer("Тег успешно удален")
    await state.clear()
