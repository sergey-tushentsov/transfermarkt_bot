"""
Модуль, содержащий класс состояний.
"""

from telebot.handler_backends import State, StatesGroup


class ValuePlayerState(StatesGroup):
    """
    Класс для состояний при выполнении команды /most_value.
    """
    teams = State()
    number = State()
