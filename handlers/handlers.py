import datetime
import os

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound
import googleapiclient

from filters import BotGroupsFilter
from keyboards import configured_google_keyboard, not_configured_google_keyboard, alarm_type_menu, alarm_type_callback, create_back_menu
from loader import dp, service, bot
from models import Group
from shedule import set_alarm_on_events
from states.states import CalendarEmail, AddEventStates, AlarmSetStates
from utils import delete_group, get_alarm, get_group, create_group, delete_group, check_email, add_event, get_future_events


@dp.message_handler(commands=['start'])
async def process_command_user(message: types.Message):
    chat_id = message.chat.id
    group: Group = await get_group(chat_id=chat_id)
    if group is None:
        group = await create_group(chat_id)
    
    keyboard = None
    if not group.google_calendar_email:
        keyboard = not_configured_google_keyboard
    else:
        keyboard = configured_google_keyboard
    await message.answer("Запуск", reply_markup=keyboard)


@dp.message_handler(BotGroupsFilter(), commands=['stop'])
async def stop_command(message: types.Message):
    try:
        chat_administrators = [admin.user.id for admin in await message.chat.get_administrators() if not admin.user.is_bot]
    except:
        is_private = True
    if is_private or message.from_user.id in chat_administrators:
        try:
            await delete_group(chat_id=message.chat.id)
            await message.answer("Остановка", reply_markup=types.ReplyKeyboardRemove())
        except:
            pass


@dp.message_handler(BotGroupsFilter(), text=['Дать доступ к Google Calendar', 'Изменить Google Calendar'])
async def access_google_account(message: types.Message):
    group: Group = await get_group(chat_id=message.chat.id)
    answer = 'Введите идентификатор своего Google Calendar (он должен быть публичным)'
    if message.text == 'Изменить Google Calendar':
        answer = answer[:-1] + f'. Текущее значение - {group.google_calendar_email})'
    await message.answer(answer, reply_markup=create_back_menu('back_gcal'))
    await CalendarEmail.email_set.set()


@dp.message_handler(BotGroupsFilter(), state=CalendarEmail.email_set)
async def set_calendar_email(message: types.Message, state: FSMContext):
    email = message.text
    answer = 'Введённый идентификатор неправильный'
    group: Group = await get_group(chat_id=message.chat.id)
    keyboard = not_configured_google_keyboard if not group.google_calendar_email else configured_google_keyboard
    if check_email(email):
        group.google_calendar_email = email
        await group.save()
        answer = 'Календарь сохранен успешно!'
        keyboard = configured_google_keyboard
    
    await message.answer(answer, reply_markup=keyboard)
    await state.finish()


@dp.message_handler(BotGroupsFilter(), text=['Получить ближайшие события из календаря Google'])
async def get_events_from_gcal(message: types.Message):
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    group: Group = await get_group(chat_id=message.chat.id)
    try:
        events_result = service.events().list(
            calendarId=group.google_calendar_email, 
            timeMin=now, singleEvents=True,
            orderBy='startTime').execute()
    except googleapiclient.errors.HttpError:
        events_result = {}
    events = events_result.get('items', [])
    answer = ''
    if not events:
        answer = 'Грядущих событий не обнаружено.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = datetime.datetime.fromisoformat(start)
        answer += f'{start.day}.{start.month}.{start.year} - {event["summary"]}\n'
    await message.answer(answer, reply_markup=configured_google_keyboard)


@dp.message_handler(BotGroupsFilter(), text=['Добавить событие'])
async def add_event_start(message: types.Message):
    await message.answer('Введите текст события', reply_markup=create_back_menu('back_event_text_set'))
    await AddEventStates.text_set.set()


@dp.message_handler(BotGroupsFilter(), state=AddEventStates.text_set)
async def add_event_add_text(message: types.Message, state: FSMContext):
    await state.update_data(event_text=message.text.capitalize())
    await message.answer(text='Напиши время события (в формате ДД.ММ.ГГГГ-ЧЧ:мм', reply_markup=create_back_menu('back_event_date_set'))
    await AddEventStates.datetime_set.set()


@dp.message_handler(BotGroupsFilter(), state=AddEventStates.datetime_set)
async def add_event_add_text(message: types.Message, state: FSMContext):
    dtime = message.text.split('-')
    if len(dtime) != 2:
        await message.reply("Пожалуйста время события в правильном формате")
        return
    dpart = dtime[0].split('.')
    tpart = dtime[1].split(':')
    if len(dpart) != 3 and len(tpart) != 2:
        await message.reply("Пожалуйста время события в правильном формате")
        return
    try:
        await state.update_data(event_dtime=datetime.datetime(
            day=int(dpart[0]), month=int(dpart[1]), year=int(dpart[2]),
            hour=int(tpart[0]), minute=int(tpart[1]), second=0))
    except ValueError:
        await message.reply("Пожалуйста время события в правильном формате")
        return
    group: Group = await get_group(chat_id=message.chat.id)
    await state.update_data(event_group=group)
    event_data = await state.get_data()
    await add_event(event_text=event_data.get('event_text'),
        event_dtime=event_data.get('event_dtime'),
        event_group=event_data.get('event_group'))
    await state.finish()
    await message.answer('Событие успешно установлено!')


@dp.message_handler(BotGroupsFilter(), text=['Просмотреть все события'])
async def get_user_events(message: types.Message):
    group: Group = await get_group(chat_id=message.chat.id)
    events = await get_future_events(group=group)
    answer = 'Все ближайшие события:\n'
    for event in events:
        answer += f'{event.text} - {event.date.day}.{event.date.month}.{event.date.year}-{event.date.hour+3}:{event.date.minute}\n'
    if not events:
        answer += 'Грядущих событий не обнаружено.'
    await message.answer(answer, reply_markup=configured_google_keyboard)


@dp.message_handler(BotGroupsFilter(), text=['Настроить напоминания'])
async def get_user_events(message: types.Message):
    await message.answer("Выберите тип оповещения", reply_markup=alarm_type_menu)
    await AlarmSetStates.alarm_type_set.set()


@dp.callback_query_handler(alarm_type_callback.filter(), state=AlarmSetStates.alarm_type_set)
async def get_chosen_alarm_type(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    alarm_type = callback_data.get('type_name')
    await state.update_data(alarm_type=alarm_type)
    await get_alarm(call, alarm_type)
    await AlarmSetStates.alarm_set.set()


@dp.message_handler(BotGroupsFilter(), state=AlarmSetStates.alarm_set)
async def get_chosen_alarm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer = await set_alarm_on_events(message.chat.id, data.get('alarm_type'), message.text)
    await message.answer(answer)
    await state.finish()


@dp.callback_query_handler(text_contains="back_", 
    state=[AlarmSetStates.alarm_type_set, AlarmSetStates.alarm_set, 
        AddEventStates.text_set, AddEventStates.datetime_set,
        CalendarEmail.email_set])
async def process_go_back(callback_query: types.CallbackQuery, state: FSMContext):
    '''
    callback for "Отмена" inline button
    '''
    await state.finish()
    try:
        await bot.delete_message(chat_id=callback_query.message.chat.id, 
            message_id=callback_query.message.message_id)
    except MessageToDeleteNotFound:
        pass
    await bot.send_message(chat_id=callback_query.message.chat.id, 
        text=f'Отмена', 
        reply_markup=configured_google_keyboard)