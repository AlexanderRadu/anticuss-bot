import re
from contextlib import suppress

import pymorphy3
from aiogram import F, Router
from aiogram.types import ContentType, Message
from rapidfuzz import fuzz

from config import BASE_BAD_WORDS, DB_NAME, LEET_COMBOS, TRANSLATION_TABLE, WHITELIST
from database import Database

router = Router()
db = Database(DB_NAME)
morph = pymorphy3.MorphAnalyzer()


def normalize(text: str) -> str:
    text = text.lower()

    for combo, replacement in LEET_COMBOS.items():
        if combo in text:
            text = text.replace(combo, replacement)

    result = []
    for char in text:
        result.append(TRANSLATION_TABLE.get(char, char))
    text = "".join(result)

    text = re.sub(r"[^а-яё]", "", text)

    return text


@router.message(F.content_type == ContentType.TEXT)
async def monitor_messages(message: Message):
    if message.chat.type == "private":
        return

    data = db.get_group_data(message.chat.id)
    if not data or data["bot_switch"] == 0:
        return
    if message.from_user.username in data["ban_list"]:
        await message.delete()
        return
    if re.search(r"(https?://\S+)", message.text):
        return

    original_text = message.text.lower()

    clean_words = re.sub(r"[^а-яёa-z\s]", "", original_text).split()
    for word in clean_words:
        forms = {word, morph.parse(word)[0].normal_form}
        if not forms.isdisjoint(BASE_BAD_WORDS) and word not in WHITELIST:
            await punish_user(message)
            return

    normalized_text = normalize(original_text)

    custom_ban_words = set(data["ban_words"])
    all_targets = BASE_BAD_WORDS.union(custom_ban_words)

    for bad_word in all_targets:
        bad_len = len(bad_word)

        if bad_len <= 3:
            if bad_word in normalized_text:
                is_safe = False
                for safe in WHITELIST:
                    if safe in normalized_text:
                        is_safe = True
                        break
                if not is_safe:
                    await punish_user(message)
                    return

        else:
            ratio = fuzz.partial_ratio(bad_word, normalized_text)

            threshold = 75 if bad_len >= 6 else 82

            if bad_len == 5:
                threshold = 79

            if ratio >= threshold:
                is_whitelisted = False
                for safe in WHITELIST:
                    if fuzz.partial_ratio(safe, normalized_text) > 90:
                        is_whitelisted = True
                        break

                if not is_whitelisted:
                    await punish_user(message)
                    return


async def punish_user(message: Message):
    with suppress(Exception):
        await message.delete()
        db.increment_mat_counter(message.chat.id)
        await message.answer(
            f"@{message.from_user.username}, ругаться запрещено!"
        )
