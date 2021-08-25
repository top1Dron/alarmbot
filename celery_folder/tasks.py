from datetime import datetime
import asyncio

from aiogram.types import message
from models import Event

from loader import bot
# from models import Chat, MessageQueue
from celery_folder.celery import app
# from utils import send_to_admin, push_message


async def push_alarm(chat: int, message):
    try:
        return await bot.send_message(chat, message)
    except:
        return


@app.task
def push_alarm_task(chat: int, event: dict):
    ed = event.get("date")
    execution_date = datetime(year=int(ed[0:4]), month=int(ed[5:7]), 
        day=int(ed[8:10]), hour=int(ed[11:13])+3, minute=int(ed[14:16]), second=0)
    message = f'Приближается событие {event.get("text")}, которое произойдёт ' \
        f'{execution_date.day}.{execution_date.month}.{execution_date.year}-{execution_date.hour}:{execution_date.minute}\n'
    coro = push_alarm(chat, message)
    asyncio.run(coro)
