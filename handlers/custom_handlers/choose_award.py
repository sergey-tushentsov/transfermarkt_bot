"""
Модуль содержит функции для предоставления пользователю информации
по полученной награде (best FIFA player) и текущему положению в списке
по другим наградам (golden boot, clean sheets).
"""

from telebot.types import Message
from loader import bot
from keyboards.inline import awards
from utils import my_requests
from handlers.custom_handlers.history import record_data


@bot.message_handler(commands=['awards'])
def start_awards(message: Message) -> None:
    """
    Обрабатывает команду /most_value. Выводит 3 inline кнопки с указанием
    типа награды. Пользователь должен выбрать одну из наград.

    :param message: сообщение пользователя.
    """
    bot.send_message(message.from_user.id,
                     'Выбери интересующую тебя награду: ',
                     reply_markup=awards.create_awards())


@bot.callback_query_handler(func=lambda callback_query: (
        callback_query.data == 'best player'))
def best_fifa_player(callback_query) -> None:
    """
    Получает данные по награде best FIFA player и выводит информацию по
    игроку, получившем эту награду в последний завершившийся сезон.

    :param callback_query: данные обратного запроса, возвращаемые при
    нажатии кнопки.
    """
    querystring = {'domain': 'com'}
    players = my_requests.api_request('statistic/list-best-fifa-players',
                                      querystring)

    record_data(callback_query.from_user.id, callback_query.from_user.username,
                'awards ({award})'.format(award=callback_query.data))

    if players:
        last_best_player = players['player'][0]

        text = (
            'Лучший игрок FIFA последнего завершившегося сезона: {player}\n'
            'Команда: {team}\n'
            'Возраст: {age}\n'
            'Текущая стоимость: {price} млн. евро'.format(
                player=last_best_player['playerName'],
                team=last_best_player['clubName'],
                age=last_best_player['ageAtThisTime'],
                price=last_best_player['marketValueAtThisTime']))

        bot.delete_message(callback_query.from_user.id,
                           callback_query.message.message_id)
        bot.send_message(callback_query.from_user.id, text)
    else:
        bot.send_message(callback_query.from_user.id,
                         'Произошла ошибка: превышено '
                         'время ожидания выполнения '
                         'запроса к API.')


@bot.callback_query_handler(func=lambda callback_query: (
        callback_query.data == 'golden boot'))
def best_fifa_player(callback_query) -> None:
    """
    Получает список из 50 игроков, которые лидируют в номинации на
    данную награду. Выводит информацию по первым 3 игрокам в списке.

    :param callback_query: данные обратного запроса, возвращаемые при
    нажатии кнопки.
    """
    querystring = {'domain': 'com'}
    players = my_requests.api_request('statistic/list-golden-boot',
                                      querystring)

    record_data(callback_query.from_user.id, callback_query.from_user.username,
                'awards ({award})'.format(award=callback_query.data))

    if players:
        header_text = ('На текущий момент первые три места в списке на '
                       'золотую бутсу занимают следующие футболисты.\n\n')
        main_text = ''

        for index in range(3):
            main_text += ('{number}. {name}\n'
                          'Количество очков: {points}\n'
                          'Количество голов: {goals}\n'
                          'Команда: {team}\n\n'.format(
                number=index + 1,
                name=players['player'][index]['playerName'],
                points=players['player'][index]['points'],
                goals=players['player'][index]['goals'],
                team=players['player'][index]['clubName']
            ))

        main_text.rstrip('\n\n')
        text = header_text + main_text

        bot.delete_message(callback_query.from_user.id,
                           callback_query.message.message_id)
        bot.send_message(callback_query.from_user.id, text)
    else:
        bot.send_message(callback_query.from_user.id,
                         'Произошла ошибка: превышено '
                         'время ожидания выполнения '
                         'запроса к API.')


@bot.callback_query_handler(func=lambda callback_query: (
        callback_query.data == 'clean sheets'))
def best_fifa_player(callback_query) -> None:
    """
    Получает список из 99 игроков (вратарей), которые лидируют в номинации на
    данную награду. Выводит информацию по первым 3 игрокам в списке.

    :param callback_query: данные обратного запроса, возвращаемые при
    нажатии кнопки.
    """
    querystring = {'domain': 'com'}
    players = my_requests.api_request('statistic/list-clean-sheets',
                                      querystring)

    record_data(callback_query.from_user.id, callback_query.from_user.username,
                'awards ({award})'.format(award=callback_query.data))

    if players:
        header_text = ('На текущий момент первые три места в списке на '
                       'золотую перчатку (больше всего "сухих" матчей) '
                       'занимают следующие вратари.\n\n')
        main_text = ''

        for index in range(3):
            main_text += ('{number}. {name}\n'
                          'Количество матчей: {appearance}\n'
                          'Количество "cухих" матчей: {clean_sheets}\n'
                          'Количество пропущенных голов: {goals_conceded}\n'
                          'Команда: {team}\n\n'.format(
                number=index + 1,
                name=players['player'][index]['playerName'],
                appearance=players['player'][index]['appearance'],
                clean_sheets=players['player'][index]['cleanSheet'],
                goals_conceded=players['player'][index]['goalsConceded'],
                team=players['player'][index]['clubName']
            ))

        main_text.rstrip('\n\n')
        text = header_text + main_text

        bot.delete_message(callback_query.from_user.id,
                           callback_query.message.message_id)
        bot.send_message(callback_query.from_user.id, text)
    else:
        bot.send_message(callback_query.from_user.id,
                         'Произошла ошибка: превышено '
                         'время ожидания выполнения '
                         'запроса к API.')
