from aiogram.dispatcher.filters.state import StatesGroup, State


class CalendarEmail(StatesGroup):
    email_set = State()


class AddEventStates(StatesGroup):
    text_set = State()
    datetime_set = State()


class AlarmSetStates(StatesGroup):
    alarm_type_set = State()
    alarm_set = State()