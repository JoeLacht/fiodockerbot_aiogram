import logging
import os
import re

from aiogram import Bot, Dispatcher
from aiogram.types import Message 
from aiogram.filters.command import Command

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)                        
dp = Dispatcher()      

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

TRANS = {
    'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'E','Ж':'ZH',
    'З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N','О':'O',
    'П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'KH','Ц':'TS',
    'Ч':'CH','Ш':'SH','Щ':'SHCH','Ь':'','Ы':'Y','Ъ':'IE','Э':'E','Ю':'IU','Я':'IA'
}

PATTERN = r"^[А-ЯЁ][а-яё]+(?:-[А-ЯЁ][а-яё]+)?(?:\s[А-ЯЁ][а-яё]+(?:-[А-ЯЁ][а-яё]+)?){1,2}$"
_re_fio = re.compile(PATTERN)

def is_valid_fio(text: str) -> bool:
    return bool(_re_fio.match(text))

def transliterate(text: str) -> str:
    parts = re.split(r'([ -])', text)
    out = []
    for part in parts:
        if part in (' ', '-'):
            out.append(part)
            continue
        res = ""
        for ch in part:
            mapped = TRANS.get(ch.upper(), ch)
            res += mapped
        out.append(res)
    return ''.join(out)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = (
        f"Привет, {user_name}! Отправь ФИО (2–3 слова на кириллице, каждое с заглавной буквы).\n"
        f"Допускаются дефисы: «Анна-Мария Смирнова-Петрова»."
    )
    logging.info(f"Инициирована команда /start от {user_name} {user_id}")
    await bot.send_message(chat_id=user_id, text=text)


@dp.message()
async def handle_fio(message: Message):
    text = message.text
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    logging.info(f"Получено сообщение от {user_name} {user_id}: {text}")

    if not is_valid_fio(text):
        help_msg = (
            "⚠ Неверный формат. Введите 2–3 слова на кириллице, каждое с заглавной буквы.\n"
            "Допускается дефис в частях имени/фамилии: «Анна-Мария Смирнова-Петрова»."
        )
        logging.warning(f"Неверный формат от {user_name} {user_id}: {text}")
        await message.answer(text=help_msg)
        return

    latin = transliterate(text)
    logging.info(f"Ответ пользователю {user_name} {user_id}: {latin}")
    await message.reply(text=latin)

if __name__ == "__main__":
    dp.run_polling(bot)

