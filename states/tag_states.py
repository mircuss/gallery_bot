from aiogram.fsm.state import State, StatesGroup


class TagStates(StatesGroup):
    add_tag = State()
    delete_tag = State()
