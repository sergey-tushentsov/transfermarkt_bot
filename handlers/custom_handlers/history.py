"""
Модуль для работы с базой данных истории запросов.
"""

import sqlite3
import os

from loader import bot
from telebot.types import Message


def path_to_db() -> str:
    """
    Вернуть абсолютный путь размещения базы данных.

    :return: путь размещения.
    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_path, "..", "..", "database", "database.db")

    db_path = os.path.abspath(db_path)

    return db_path


def record_data(id_user: int, name: str, query: str) -> None:
    """
    Выполнить запись в базу данных history.

    :param id_user: id пользователя.
    :param name: имя пользователя.
    :param query: наименование выполненного запроса.
    """
    db_path = path_to_db()

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS history "
            "(id INTEGER, name TEXT, "
            "date TEXT DEFAULT CURRENT_TIMESTAMP, query TEXT)")

        data = (id_user, name, query)

        cursor.execute("INSERT INTO history (id, name, query)"
                       "VALUES (?, ?, ?)", data)
        conn.commit()


@bot.message_handler(commands=['history'])
def show_history(message: Message) -> None:
    """
    Вернуть историю запросов из базы данных для конкретного пользователя.

    :param message: сообщение пользователя.
    """
    db_path = path_to_db()

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT datetime(date, 'localtime'), query FROM "
                       "history WHERE id = ?", [message.from_user.id])

        text = ''
        number = 1

        for row in cursor:
            text += '{number}. {date} - запрос: {query}\n'.format(
                number=str(number),
                date=row[0],
                query=row[1]
            )
            number += 1

        conn.commit()

    text.rstrip('\n')
    bot.send_message(message.from_user.id, 'Ваша история запросов: \n'
                                           '{history}'.format(history=text))
