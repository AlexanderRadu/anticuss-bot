from aiogram.types import Message
from aiogram import Bot

async def is_admin(message: Message, bot: Bot) -> bool:
    if message.chat.type == 'private':
        return False
    try:
        admins = await bot.get_chat_administrators(message.chat.id)
        admin_ids = [admin.user.id for admin in admins]
        return message.from_user.id in admin_ids
    except:
        return False