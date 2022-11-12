from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_subscribe_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton('Подписаться', callback_data='subscribe')
    )

    return keyboard


def get_info_suggest_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton('Да', callback_data='info_yes'), 
        InlineKeyboardButton('Нет', callback_data='info_no'),
    )

    return keyboard


def get_survey_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton('К анкете', callback_data='to_survey')
    )
    
    return keyboard

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton('Отмена', callback_data='cancel')
    )

    return keyboard

