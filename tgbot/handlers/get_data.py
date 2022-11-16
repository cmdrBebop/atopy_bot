from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from tgbot.misc.states import SurveyState

import tgbot.keyboards.inline as inline_keyboard
from tgbot.services.google_sheets import GoogleSheets
from tgbot.services.mindbox import MindBox
from tgbot.services.mindbox.schemas import CustomerData, APIError, InvalidEmail, InvalidPhoneNumber, CustomData


async def info_suggest(call: CallbackQuery):
    await call.message.edit_text('Хочешь получать информацию о наших мероприятиях, подкастах, скидках и других приятных бонусах?', reply_markup=inline_keyboard.get_info_suggest_keyboard())
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
    mindbox = call.bot.get('mindbox')
    google_sheets = call.bot.get('google_sheets')
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
    await register_customer(mindbox, google_sheets, call.message, call.from_user.id, full_name, email)


async def get_phone_number(message: Message, state: FSMContext):
    mindbox = message.bot.get('mindbox')
    google_sheets = message.bot.get('google_sheets')
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

    await register_customer(mindbox, google_sheets, message, message.from_id, full_name, email, phone_number)


async def register_customer(mindbox: MindBox, google_sheets: GoogleSheets, message: Message, telegram_id, full_name, email, phone_number=''):
    fio = full_name.split()
    if len(fio) != 3:
        await message.answer('Неверно указано ФИО. Попробуйте ещё раз.')
        return

    last_name, first_name, middle_name = fio

    customer = CustomerData(
        email=email,
        lastName=last_name,
        firstName=first_name,
        middleName=middle_name,
        mobilePhone=phone_number,
        customFields=CustomData(
            customerTelegramId=telegram_id
        )
    )

    try:
        result = await mindbox.register_customer_with_telegram_bot(customer)
    except APIError:
        await message.answer('Что-то пошло не так. Попробуйте позже или свяжитесь с администратором.')
    except InvalidEmail:
        await message.answer('Неверно указана почта. Попробуйте ещё раз.')
    except InvalidPhoneNumber:
        await message.answer('Неверно указан номер телефона. Попробуйте ещё раз.')
    else:
        if result:
            google_sheets.add_customer(full_name, email, phone_number)
        else:
            await message.answer('Что-то пошло не так. Попробуйте позже или свяжитесь с администратором.')


def register_main(dp: Dispatcher):
    dp.register_callback_query_handler(info_suggest, text='subscribe')
    dp.register_callback_query_handler(no_info_suggest, text='info_no')
    dp.register_callback_query_handler(yes_info_suggest, text='info_yes')
    dp.register_callback_query_handler(input_full_name, text='to_survey')
    dp.register_message_handler(get_full_name, state=SurveyState.waiting_for_full_name)
    dp.register_message_handler(get_email, state=SurveyState.waiting_for_email)
    dp.register_callback_query_handler(get_no_phone_number, text='no_phone', state='*')
    dp.register_message_handler(get_phone_number, state=SurveyState.waiting_for_phone_number) 
