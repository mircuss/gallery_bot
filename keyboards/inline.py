from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_tag_keyboard(tags: list, last: int) -> InlineKeyboardMarkup:
    keyboard = []
    for tag in tags:
        print(tag[0])
        print(tag[0].name)
        button = InlineKeyboardButton(text=tag[0].name,
                                      callback_data=f"tag_{tag[0].id}")
        keyboard.append([button])
    keyboard.append([
        InlineKeyboardButton(text="Назад", callback_data=f"prev_{last}"),
        InlineKeyboardButton(text="Вперед", callback_data=f"next_{last}")
    ])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup
