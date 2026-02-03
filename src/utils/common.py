from contextlib import suppress

from aiogram import Bot
from aiogram.types import Message


async def is_admin(message: Message, bot: Bot) -> bool | None:
    if message.chat.type == 'private':
        return False
    with suppress(Exception):
        admins = await bot.get_chat_administrators(message.chat.id)
        admin_ids = [admin.user.id for admin in admins]
        return message.from_user.id in admin_ids
    return False
