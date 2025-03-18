"""
Модуль содержит обработчик команды /help.
"""

from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    """
    Обработчик команды /help. Выводит пользователю список
    имеющихся у бота команд.

    :param message: сообщение пользователя.
    """
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
