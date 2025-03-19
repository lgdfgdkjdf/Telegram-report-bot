import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ChatType
from aiogram.utils import executor
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("7705193251:AAFQPcT5iNqlu4bnlcjV_lYjjZ7GZWzZHj4")
ADMIN_CHAT_ID = os.getenv("-1002651165474")  # ID группы для администрации

# Настройка бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    await message.reply("Привет! Отправь /report @username причина, чтобы пожаловаться на пользователя.")

@dp.message_handler(commands=['report'])
async def report_command(message: Message):
    if message.chat.type != ChatType.SUPERGROUP:
        await message.reply("Команда доступна только в группах.")
        return
    
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.reply("Использование: /report @username причина")
        return
    
    username = args[1]
    reason = args[2]
    report_text = (f"🚨 *Новый репорт!*
📌 Пользователь: {username}
❗ Причина: {reason}
👤 Отправитель: @{message.from_user.username}")
    
    await bot.send_message(ADMIN_CHAT_ID, report_text, parse_mode="Markdown")
    await message.reply("Репорт отправлен администрации!")

if __name__ == "__main__":

    executor.start_polling(dp, skip_updates=True)
