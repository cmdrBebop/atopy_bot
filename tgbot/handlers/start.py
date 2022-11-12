from aiogram import Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
import tgbot.keyboards.inline as inline_keyboard


async def start(message: Message):
    menu_message = '''
    Привет! Это бот #уАтопииЕстьЛицо. Он поможет тебе попасть в телеграм-канал, который мы сделали для пациентов с атопическим дерматитом и родителей детей с этим заболеванием. 


ТГ-канал #уАтопииЕстьЛицо — место, где благодаря знаниям и поддержке экспертов, вы сможете разобраться в этом заболевании. Нам важно, чтобы знания, которые вы  получите тут, научили вас контролировать заболевание, помогли вам испытать облегчение и обрести уверенность в том, что вы делаете все правильно.

Вокруг атопического дерматита много мифов, и наша миссия – развеять их и научить вас жить с этим заболеванием! 

Вы с нами? 
    '''

    await message.delete()
    await message.answer(menu_message, reply_markup=inline_keyboard.get_subscribe_keyboard())


async def cancel(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text('Menu', reply_markup=inline_keyboard.get_menu_keyboard())


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_callback_query_handler(cancel, text='cancel', state='*')
