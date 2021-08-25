from datetime import datetime, timedelta
from typing import Iterable

import aioschedule as schedule

from celery_folder.tasks import push_alarm_task
from models import Event
from utils import get_future_events, get_group


async def by_minutes(minute: int, chat_id, events: Iterable[Event]):
    if  0 < minute < 1440:
        for event in events:
            push_alarm_task.apply_async((chat_id, event.as_dict),
                eta=datetime.today().replace(
                    year=event.date.year,
                    month=event.date.month,
                    day=event.date.day,
                    hour=event.date.replace(hour=event.date.hour).hour,
                    minute=(event.date - timedelta(minutes=minute)).minute))
    else:
        raise ValueError


async def by_hours(hour: int, chat_id, events: Iterable[Event]):
    if 0 < hour < 24:
        for event in events:
            push_alarm_task.apply_async((chat_id, event.as_dict),
                eta=datetime.today().replace(
                    year=event.date.year,
                    month=event.date.month,
                    day=event.date.day,
                    hour=(event.date - timedelta(hours=hour)).hour,
                    minute=event.date.minute))
    else:
        raise ValueError


async def set_alarm_on_events(chat_id: int, alarm_type: str, alarm: str):
    schedule.clear(str(chat_id))
    events = await get_future_events(await get_group(chat_id))
    if alarm_type == 'from_morning' or alarm_type == 'from_evening':
        try:
            if 1 > int(alarm) > 12:
                raise ValueError
            if alarm_type == 'from_evening':
                alarm = str(int(alarm) + 12)
            for event in events:
                push_alarm_task.apply_async((chat_id, event.as_dict),
                                                eta=event.date.replace(hour=int(alarm)))
        except ValueError:
            return "Час должен быть настроен в диапазоне от 1 до 12"
    if alarm_type == 'by_time':
        alarm_list = alarm.split(":")
        alarm_dict = {
            'минута': by_minutes,
            'час': by_hours
        }
        try:
            await alarm_dict[alarm_list[1]](int(alarm_list[0]), chat_id, events)
        except KeyError:
            return 'Неправильный формат число:тип (без пробелов)'
        except ValueError:
            return "Введённое число должно быть больше 0 и меньше суток в общем!"
    return "Оповещения настроены"
