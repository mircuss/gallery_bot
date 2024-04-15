from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_tag_keyboard(tags: list,
                          last: int,
                          message_id: int,
                          pre: str = "") -> InlineKeyboardMarkup:
    keyboard = []
    for tag in tags:
        print(tag[0])
        print(tag[0].name)
        button = InlineKeyboardButton(text=tag[0].name,
                                      callback_data=(f"{pre}tag_{tag[0].id}"
                                                     f"_{message_id}"))
        keyboard.append([button])
    keyboard.append([
        InlineKeyboardButton(text="Назад",
                             callback_data=f"{pre}prev_{last}_{message_id}"),
        InlineKeyboardButton(text="Вперед",
                             callback_data=f"{pre}next_{last}_{message_id}")
    ])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup
