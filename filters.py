from aiogram import types
from aiogram.dispatcher.filters import Filter

from utils import get_bot_groups

class BotGroupsFilter(Filter):
    key = 'chat_id'

    async def check(self, message: types.Message) -> bool:
        return message.chat.id in await get_bot_groups()