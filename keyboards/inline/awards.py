"""
Модуль, содержащий функцию создания inline клавиатуру.
"""

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_awards():
    """
    Создать и вернуть inline клавиатуру с 3 кнопками.

    :return: inline клавиатуру.
    """
    best_player = InlineKeyboardButton(text='best FIFA player 🏆',
                                       callback_data='best player')
    golden_boot = InlineKeyboardButton(text='golden boot ⚽️',
                                       callback_data='golden boot')
    clean_sheets = InlineKeyboardButton(text='clean sheets 👐',
                                        callback_data='clean sheets')

    keyboard = InlineKeyboardMarkup()
    keyboard.add(best_player)
    keyboard.add(golden_boot)
    keyboard.add(clean_sheets)

    return keyboard
