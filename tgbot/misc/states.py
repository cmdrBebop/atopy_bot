from aiogram.dispatcher.filters.state import State, StatesGroup


class SurveyState(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_email = State()
    waiting_for_phone_number = State()

