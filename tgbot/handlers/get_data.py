from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from tgbot.misc.states import SurveyState

import tgbot.keyboards.inline as inline_keyboard


async def info_suggest(call: CallbackQuery):
    await call.message.edit_text('Хотите получать дополнительную инфомацию?', reply_markup=inline_keyboard.get_info_suggest_keyboard())
    await call.answer()


async def no_info_suggest(call: CallbackQuery):
    db = call.bot.get('database')
    await call.message.edit_text(await db.messages_worker.get_message(0), reply_markup=inline_keyboard.get_menu_keyboard(await db.messages_worker.get_message(1)))
    await call.answer()

    
async def yes_info_suggest(call: CallbackQuery):
    await call.message.edit_text('Ура! Заполни, пожалуйста, небольшую анкету', reply_markup=inline_keyboard.get_survey_keyboard())
    await call.answer()

async def input_full_name(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Введите ФИО', reply_markup=inline_keyboard.get_cancel_keyboard())
    await state.update_data(prev_menu_id=call.message.message_id)
    await SurveyState.waiting_for_full_name.set()
    await call.answer()


async def get_full_name(message: Message, state: FSMContext):
    full_name = message.text
    state_data = await state.get_data()
    prev_menu_id = state_data['prev_menu_id']

    await message.delete()

    await state.update_data(full_name=full_name)
    await SurveyState.waiting_for_email.set()
    await message.bot.edit_message_text(
        chat_id=message.from_id,
        message_id=prev_menu_id,
        text='Отлично! Теперь введите почту',
        reply_markup=inline_keyboard.get_cancel_keyboard()
    )


async def get_email(message: Message, state: FSMContext):
    email = message.text

    state_data = await state.get_data()
    prev_menu_id = state_data['prev_menu_id']

    await message.delete()

    await state.update_data(email=email)
    await SurveyState.waiting_for_phone_number.set()
    await message.bot.edit_message_text(
        chat_id=message.from_id,
        message_id=prev_menu_id,
        text='Замечательно! Ниже по желанию вы можете оставить номер телефона. Вводите номер в международном формате. Например +79998887766',
        reply_markup=inline_keyboard.get_phone_cancel_keyboard()
    )


async def get_no_phone_number(call: CallbackQuery, state: FSMContext):
    db = call.bot.get('database')
    
    state_data = await state.get_data()
    
    await state.finish()

    full_name = state_data['full_name'] 
    email = state_data['email']

    # add to db full_name/email/phone_number

    await call.message.edit_text(
        text=f'Благодарим за заполнение анкеты! Ваши данные: {full_name}, {email}',
        reply_markup=inline_keyboard.get_link_keyboard(await db.messages_worker.get_message(1))
    )

    await call.answer()



async def get_phone_number(message: Message, state: FSMContext):
    db = message.bot.get('database')
    phone_number = message.text
    
    state_data = await state.get_data()
    prev_menu_id = state_data['prev_menu_id']
    
    await message.delete()
    await state.finish()

    full_name = state_data['full_name'] 
    email = state_data['email']

    # add to db full_name/email/phone_number

    await message.bot.edit_message_text(
        chat_id=message.from_id,
        message_id=prev_menu_id,
        text=f'Благодарим за заполнение анкеты! Ваши данные: {full_name}, {email}, {phone_number}',
        reply_markup=inline_keyboard.get_link_keyboard(await db.messages_worker.get_message(1))
    )


def register_main(dp: Dispatcher):
    dp.register_callback_query_handler(info_suggest, text='subscribe')
    dp.register_callback_query_handler(no_info_suggest, text='info_no')
    dp.register_callback_query_handler(yes_info_suggest, text='info_yes')
    dp.register_callback_query_handler(input_full_name, text='to_survey')
    dp.register_message_handler(get_full_name, state=SurveyState.waiting_for_full_name)
    dp.register_message_handler(get_email, state=SurveyState.waiting_for_email)
    dp.register_callback_query_handler(get_no_phone_number, text='no_phone', state='*')
    dp.register_message_handler(get_phone_number, state=SurveyState.waiting_for_phone_number) 
