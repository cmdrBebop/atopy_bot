from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

import tgbot.keyboards.inline as inline_keyboard


async def info_suggest(call: CallbackQuery):
    await call.message.edit_text('Хотите получать дополнительную инфомацию?', reply_markup=inline_keyboard.get_info_suggest_keyboard())
    await call.answer()


async def no_info_suggest(call: CallbackQuery):
    await call.message.answer('ссылочка')
    await call.answer()

    
async def yes_info_suggest(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Ура! Заполни, пожалуйста, небольшую анкету', reply_markup=inline_keyboard.get_survey_keyboard())
    await call.answer()


def register_main(dp: Dispatcher):
    dp.register_callback_query_handler(info_suggest, state='subscribe')
    dp.register_callback_query_handler(no_info_suggest, state='info_no')
