"""
Модуль содержит обработчик сообщений без указанного состояния.
"""

from telebot.types import Message

from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message):
    """
    Отвечает на все сообщения без указанного состояния.

    :param message: сообщение пользователя.
    """
    bot.reply_to(
        message,
        "Эхо без состояния или фильтра.\n" f"Сообщение: {message.text}"
    )
