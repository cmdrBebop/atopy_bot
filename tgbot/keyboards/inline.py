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


def get_phone_cancel_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton('Не хочу оставлять телефон', callback_data='no_phone'),
        InlineKeyboardButton('Отмена', callback_data='cancel')
    )

    return keyboard


def get_menu_keyboard(link: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton('Ссылка', url=link),
        InlineKeyboardButton('К анкете', callback_data='to_survey')
    )

    return keyboard


def get_link_keyboard(link: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton('Ссылка', url=link)
    )

    return keyboard


def get_admin_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton('Поменять приветстие', callback_data='change_greetings'),
        InlineKeyboardButton('Поменять ссылку на канал', callback_data='change_chanel_link')
    )

    return keyboard


def get_back_to_admin_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton('Назад', callback_data='back_to_admin')
    )

    return keyboard

