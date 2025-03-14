from telebot.types import Message
from loader import bot
from keyboards.inline import awards
from utils import my_requests


@bot.message_handler(commands=['awards'])
def start_awards(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     'Выбери интересующую тебя награду: ',
                     reply_markup=awards.create_awards())


@bot.callback_query_handler(func=lambda callback_query: (
        callback_query.data == 'best player'))
def best_fifa_player(callback_query) -> None:
    querystring = {'domain': 'com'}
    players = my_requests.api_request('statistic/list-best-fifa-players',
                                      querystring)

    last_best_player = players['player'][0]

    text = ('Лучший игрок FIFA последнего завершившегося сезона: {player}\n'
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


@bot.callback_query_handler(func=lambda callback_query: (
        callback_query.data == 'golden boot'))
def best_fifa_player(callback_query) -> None:
    querystring = {'domain': 'com'}
    players = my_requests.api_request('statistic/list-golden-boot',
                                      querystring)

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


@bot.callback_query_handler(func=lambda callback_query: (
        callback_query.data == 'clean sheets'))
def best_fifa_player(callback_query) -> None:
    querystring = {'domain': 'com'}
    players = my_requests.api_request('statistic/list-clean-sheets',
                                      querystring)

    header_text = ('На текущий момент первые три места в списке на '
                   'золотую перчатку (больше всего "сухих" матчей) занимают '
                   'следующие вратари.\n\n')
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
