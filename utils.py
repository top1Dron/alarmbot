from datetime import datetime
import pytz
import re

from typing import Iterable, Union
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from tortoise.exceptions import DoesNotExist

from keyboards import chat_callback, create_back_menu
from loader import bot
from models import Group, Event
# , Chat, MessageQueue
from settings import admin_id


local_tz = pytz.timezone('Europe/Kiev')


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("stop", "Остановить бота"),
    ])

async def get_group(chat_id: Union[int, str]) -> Group:
    return await Group.filter(chat_id=str(chat_id)).first()


async def create_group(chat_id: Union[int, str]) -> Group:
    new_group = await Group.create(chat_id=str(chat_id))
    return new_group


async def get_bot_groups() -> Iterable[int]:
    return [int(group.chat_id) for group in await Group.all()]


async def delete_group(chat_id: Union[int, str]) -> None:
    group = await get_group(chat_id=chat_id)
    await group.delete()


def check_email(email: str):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	# pass the regular expression
	# and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False


async def add_event(event_text: str, event_dtime: datetime, event_group: Group):
    event = await Event.create(text=event_text, date=local_tz.localize(event_dtime), group=event_group)
    return event


async def get_future_events(group):
    return await Event.filter(group=group, date__gt=datetime.now())


async def get_alarm(call: CallbackQuery, alarm_type: str):
    alarm_type_list = {
        'from_morning': 'Укажите час оповещения, числом от 1 до 12',
        'from_evening': 'Укажите час оповещения, числом от 1 до 12',
        'by_time': 'Укажите, за сколько времени до события вас оповестить в формате "число:тип времени. "'
            'тип времени [минута, час]',
    }
    await call.message.edit_text(alarm_type_list[alarm_type], reply_markup=create_back_menu('back_alarm_set'))