import os
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from database import Database
from config import DB_NAME
from utils.common import is_admin
from utils.graphs import generate_stats_graph

router = Router()
db = Database(DB_NAME)

@router.message(Command("start"))
async def cmd_start(message: Message, bot: Bot):
    if message.chat.type == 'private':
        await message.answer("Бот работает только в групповых чатах!")
        return

    if await is_admin(message, bot):
        db.add_group(message.chat.id, message.chat.title)
        await message.answer("Бот запущен!")

@router.message(Command("help"))
async def cmd_help(message: Message, bot: Bot):
    if await is_admin(message, bot):
        text = (
            "Команды бота:\n"
            "/ban @ник - Добавить в ЧС\n"
            "/unban @ник - Удалить из ЧС\n"
            "/banlist - Список ЧС\n"
            "/add [слово] - Запретить слово\n"
            "/del [слово] - Разрешить слово\n"
            "/info - Статистика\n"
            "/stop - Выключить бота\n"
            "/start - Включить бота"
        )
        await message.reply(text)

@router.message(Command("stop"))
async def cmd_stop(message: Message, bot: Bot):
    if await is_admin(message, bot):
        db.set_bot_switch(message.chat.id, 0)
        await message.reply("Бот выключен!")

@router.message(Command("info"))
async def cmd_info(message: Message, bot: Bot):
    if not await is_admin(message, bot):
        return

    total_mat, df = db.get_stats()
    group_data = db.get_group_data(message.chat.id)

    if not group_data:
        await message.reply("Нет данных о группе. Нажмите /start")
        return

    this_chat_mat = group_data['mat_counter']
    percent = (this_chat_mat * 100 / total_mat) if total_mat > 0 else 0

    photo_path = await generate_stats_graph(df)

    caption = (
        f"Всего заблокировано сообщений: {total_mat}\n"
        f"Этот чат: {this_chat_mat} ({percent:.1f}%)\n"
        "График: Топ 10 групп."
    )

    photo = FSInputFile(photo_path)
    await message.answer_photo(photo, caption=caption)

    os.remove(photo_path)