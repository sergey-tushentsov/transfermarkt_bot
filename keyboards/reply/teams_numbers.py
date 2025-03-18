"""
Модуль, содержащий функцию создания reply клавиатуры.
"""

from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def create_numbers(count: int):
    """
    Создать и вернуть клавиатуру с числами от 1 до count.

    :param count: количество команд.
    :return: reply клавиатура.
    """
    numbers = [str(number) for number in range(1, count + 1)]

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(number) for number in numbers]

    keyboard.add(*buttons)

    return keyboard
