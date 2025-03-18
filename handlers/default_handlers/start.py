"""
Модуль содержит обработчик команды /start.
"""

from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    """
    Обработчик команды /start. Приветствует пользователя и выводит
    информацию о назначении бота.

    :param message: сообщение пользователя.
    """
    bot.reply_to(message, f"Привет, {message.from_user.full_name}! "
                          f"Я бот, который предоставляет статистическую "
                          f"информацию для любителей футбола с портала "
                          f"Transfermarkt. Выберите из имеющихся команд, "
                          f"чтобы Вы хотели узнать.")
