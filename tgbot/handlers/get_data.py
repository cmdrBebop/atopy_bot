from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from tgbot.misc.states import SurveyState

import tgbot.keyboards.inline as inline_keyboard


async def info_suggest(call: CallbackQuery):
    await call.message.edit_text('Хотите получать дополнительную инфомацию?', reply_markup=inline_keyboard.get_info_suggest_keyboard())
    await call.answer()


async def no_info_suggest(call: CallbackQuery):
    await call.message.answer('ссылочка')
    await call.answer()

    
async def yes_info_suggest(call: CallbackQuery):
    await call.message.edit_text('Ура! Заполни, пожалуйста, небольшую анкету', reply_markup=inline_keyboard.get_survey_keyboard())
    await call.answer()

async def input_full_name(call: CallbackQuery):
    await call.message.edit_text('Введите ФИО', reply_markup=inline_keyboard.get_cancel_keyboard())
    await SurveyState.waiting_for_full_name.set()
    await call.answer()


async def get_full_name(message: Message, state: FSMContext):
    full_name = message.text

    await message.delete()

    await state.update_data(full_name=full_name)
    await SurveyState.waiting_for_email.set()
    await message.bot.edit_message_text(
        chat_id=message.from_id,
        message_id=...,
        text='Отлично! Теперь введите почту' 
    )


def register_main(dp: Dispatcher):
    dp.register_callback_query_handler(info_suggest, state='subscribe')
    dp.register_callback_query_handler(no_info_suggest, state='info_no')
