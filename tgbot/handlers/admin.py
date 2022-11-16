from aiogram import Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
import tgbot.keyboards.inline as inline_keyboard

from tgbot.misc.states import GreetingsState, LinkState

async def admin(message: Message):
    await message.delete()
    await message.answer('Админ-меню', reply_markup=inline_keyboard.get_admin_menu_keyboard())


async def change_greetings(call: CallbackQuery, state: FSMContext):
    db = call.bot.get('database')
    await call.message.edit_text((await db.messages_worker.get_message(0)) + '\nВы можете поменять текст приветствия введя новый ниже', reply_markup=inline_keyboard.get_back_to_admin_menu_keyboard())
    
    await state.update_data(prev_menu_id=call.message.message_id)
    await GreetingsState.waiting_for_greetings.set()
    await call.answer()


async def get_greetings(message: Message, state: FSMContext):
    new_greetings = message.text
    state_data = await state.get_data()
    prev_menu_id = state_data['prev_menu_id']

    await message.delete()
    await state.finish()

    db = message.bot.get('database')
    await db.messages_worker.update_message(0, new_greetings)
    
    await message.bot.edit_message_text(
        chat_id=message.from_id,
        message_id=prev_menu_id,
        text=f'Текст приветствия изменен на: {new_greetings}',
        reply_markup=inline_keyboard.get_back_to_admin_menu_keyboard()
    )



async def change_chanel_link(call: CallbackQuery, state: FSMContext):
    db = call.bot.get('database')

    await call.message.edit_text((await db.messages_worker.get_message(1)) + '\nВы можете поменять ссылку на канал введя новую ниже', reply_markup=inline_keyboard.get_back_to_admin_menu_keyboard())

    await state.update_data(prev_menu_id=call.message.message_id)
    await LinkState.waiting_for_link.set()
    await call.answer()


async def get_chanel_link(message: Message, state: FSMContext):
    new_link = message.text
    state_data = await state.get_data()
    prev_menu_id = state_data['prev_menu_id']

    await message.delete()
    await state.finish()

    db = message.bot.get('database')
    await db.messages_worker.update_message(1, new_link)
    
    await message.bot.edit_message_text(
        chat_id=message.from_id,
        message_id=prev_menu_id,
        text=f'Ссылка изменена на: {new_link}',
        reply_markup=inline_keyboard.get_back_to_admin_menu_keyboard()
    )


async def back_to_admin_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text('Админ-меню', reply_markup=inline_keyboard.get_admin_menu_keyboard())
    await call.answer()

def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin, commands=['admin'], state="*")
    dp.register_callback_query_handler(change_greetings, text='change_greetings')
    dp.register_message_handler(get_greetings, state=GreetingsState.waiting_for_greetings)
    dp.register_callback_query_handler(back_to_admin_menu, text='back_to_admin', state='*') 
    dp.register_callback_query_handler(change_chanel_link, text='change_chanel_link')
    dp.register_message_handler(get_chanel_link, state=LinkState.waiting_for_link)
    
