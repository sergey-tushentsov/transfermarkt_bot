from typing import List, Any, Dict

from telebot.types import Message, ReplyKeyboardRemove
from states.value_states import ValuePlayerState
from loader import bot
from keyboards.reply import teams_numbers
from utils import my_requests


def find_teams(team: str) -> Dict[int, List[Any]]:
    """
    Вернуть словарь с id и наименованием подходящих команд.

    :param team: наименование команды.
    :return: словарь с командами и их id.
    """

    querystring = {"query": team, "domain": "com"}
    json_data = my_requests.api_request('search', querystring)

    data_team = dict()
    number = 1
    for team in json_data['clubs']:
        data_team[number] = [team['id'], team['name']]
        number += 1

    return data_team


def find_all_players(team_id: str) -> dict[int, List[Any]]:
    """
    Вернуть словарь, содержащий всех игроков конкретной команды.

    :param team_id: id выбранной команды.
    :return: словарь со всеми игроками.
    """

    querystring = {"id": team_id, "saison_id": 2025, "domain": "com"}
    json_data = my_requests.api_request('clubs/get-squad', querystring)

    return json_data


@bot.message_handler(commands=['most_value'])
def user_team(message: Message) -> None:
    bot.set_state(message.from_user.id, ValuePlayerState.teams,
                  message.chat.id)
    bot.send_message(message.from_user.id, 'Введи интересующую тебя '
                                           'команду латинскими буквами.')


@bot.message_handler(state=ValuePlayerState.teams)
def get_teams(message: Message) -> None:
    bot.set_state(message.from_user.id, ValuePlayerState.number,
                  message.chat.id)
    teams = find_teams(message.text)
    text = ''

    for number, team in teams.items():
        text += str(number) + '. ' + team[1] + '\n'

    text.rstrip('\n')
    bot.send_message(message.from_user.id, text)
    bot.send_message(message.from_user.id, 'Введи номер интересующей тебя '
                                           'команды.',
                     reply_markup=teams_numbers.create_numbers(len(teams)))
    bot.add_data(message.from_user.id, message.chat.id, teams=teams)


@bot.message_handler(state=ValuePlayerState.number)
def get_player(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id) as data:
        if int(message.text) <= len(data['teams']):
            id_team = data['teams'][int(message.text)][0]
            team_name = data['teams'][int(message.text)][1]

            players = find_all_players(id_team)

            data['name'] = players['squad'][0]['name']
            data['price'] = players['squad'][0]['marketValue']['value']
            data['age'] = players['squad'][0]['age']

            for player in players['squad'][1:]:
                if data['price'] < player['marketValue']['value']:
                    data['price'] = player['marketValue']['value']
                    data['name'] = player['name']
                    data['age'] = player['age']

            text = ('Самый ценный игрок в команде {team} - {name}.\n'
                    'Стоимость: {price} млн евро\n'
                    'Возраст: {age} года \\ лет\n'.format(
                team=team_name,
                name=data['name'],
                price=f"{data['price'] / 1_000_000:.3f}",
                age=data['age']))

            bot.send_message(message.from_user.id, text,
                             reply_markup=ReplyKeyboardRemove())
            bot.delete_state(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Вы ввели неверный '
                                                   'номер команды.',
                             reply_markup=ReplyKeyboardRemove())
            bot.delete_state(message.from_user.id, message.chat.id)
