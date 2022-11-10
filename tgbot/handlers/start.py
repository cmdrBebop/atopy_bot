from aiogram import Dispatcher
from aiogram.types import Message
import tgbot.keyboards.inline as inline_keyboard


async def start(message: Message):
    await message.answer('Autopia hello', reply_markup=inline_keyboard.get_subscribe_keyboard())


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
