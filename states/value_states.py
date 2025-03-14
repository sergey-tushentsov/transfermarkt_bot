from telebot.handler_backends import State, StatesGroup


class ValuePlayerState(StatesGroup):
    teams = State()
    number = State()
