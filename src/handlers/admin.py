from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message

from config import DB_NAME
from database import Database
from utils.common import is_admin

router = Router()
db = Database(DB_NAME)

@router.message(Command("ban"))
async def cmd_ban(message: Message, bot: Bot):
    if not await is_admin(message, bot):
        return

    if "@" not in message.text or len(message.text.split()) < 2:
        await message.reply("Используйте: /ban @ник")
        return

    username = message.text.split("@")[1].strip()

    admins = await bot.get_chat_administrators(message.chat.id)
    admin_usernames = [a.user.username for a in admins if a.user.username]

    if username in admin_usernames:
        await message.reply("Нельзя забанить администратора.")
        return

    data = db.get_group_data(message.chat.id)
    current_list = data['ban_list']

    if username not in current_list:
        current_list.append(username)
        db.update_ban_list(message.chat.id, current_list)
        await message.reply(f"@{username} добавлен в черный список.")
    else:
        await message.reply("Пользователь уже в черном списке.")

@router.message(Command("unban"))
async def cmd_unban(message: Message, bot: Bot):
    if not await is_admin(message, bot):
        return

    if "@" not in message.text:
        await message.reply("Используйте: /unban @ник")
        return

    username = message.text.split("@")[1].strip()
    data = db.get_group_data(message.chat.id)
    current_list = data['ban_list']

    if username in current_list:
        current_list.remove(username)
        db.update_ban_list(message.chat.id, current_list)
        await message.reply(f"@{username} разблокирован.")
    else:
        await message.reply("Пользователя нет в черном списке.")

@router.message(Command("banlist"))
async def cmd_banlist(message: Message, bot: Bot):
    if not await is_admin(message, bot):
        return

    data = db.get_group_data(message.chat.id)
    if data and data['ban_list']:
        await message.reply("Забаненные: " + ", ".join(data['ban_list']))
    else:
        await message.reply("Список пуст.")

@router.message(Command("add"))
async def cmd_add_word(message: Message, bot: Bot):
    if not await is_admin(message, bot):
        return

    args = message.text.split()
    if len(args) != 2:
        await message.reply("Используйте: /add [слово]")
        return

    word = args[1].lower()
    data = db.get_group_data(message.chat.id)
    words = data['ban_words']

    if word not in words:
        words.append(word)
        db.update_ban_words(message.chat.id, words)
        await message.reply(f"Слово '{word}' добавлено.")
    else:
        await message.reply("Слово уже есть в списке.")

@router.message(Command("banwords"))
async def cmd_wordlist(message: Message, bot: Bot):
    if not await is_admin(message, bot):
        return
    data = db.get_group_data(message.chat.id)
    if data and data['ban_words']:
        await message.reply("Запрещенные слова: " + ", ".join(data['ban_words']))
    else:
        await message.reply("Список слов пуст.")
