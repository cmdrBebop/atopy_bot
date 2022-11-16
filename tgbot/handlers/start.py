from aiogram import Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
import tgbot.keyboards.inline as inline_keyboard


async def start(message: Message):
    db = message.bot.get('database')
    await message.delete()
    await message.answer(await db.messages_worker.get_message(0), reply_markup=inline_keyboard.get_subscribe_keyboard())


async def cancel(call: CallbackQuery, state: FSMContext): 
    db = call.bot.get('database')
    await state.finish()
    await call.message.edit_text(await db.messages_worker.get_message(0), reply_markup=inline_keyboard.get_menu_keyboard(await db.messages_worker.get_message(1)))


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_callback_query_handler(cancel, text='cancel', state='*')
