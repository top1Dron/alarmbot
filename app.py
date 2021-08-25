import asyncio

from aiogram import executor
from tortoise import Tortoise
import aioschedule as schedule

from filters import BotGroupsFilter
from loader import dp
from settings import db_url
from utils import set_default_commands
import handlers


async def scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['models']},
    )
    await Tortoise.generate_schemas()
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    dp.bind_filter(BotGroupsFilter)
    executor.start_polling(dp, on_startup=on_startup)
