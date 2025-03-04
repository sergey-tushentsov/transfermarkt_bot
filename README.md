### Описание проекта
Telegram-бот для получения информации с портала transfermarkt.

### Как запустить
Для корректной работы бота необходимо в корне проекта создать виртуальное окружение.
Виртуальное окружение для ОС Windows можно создать следующей командой в командной
строке:  
py -m venv .venv  
Активировать виртуальное окружение можно в командной строке командой:  
.venv\Scripts\activate  

Далее необходимо установить 3 библиотеки: pyTelegramBotAPI, python-dotenv, requests. Все 
необходимые библиотеки можно установить с помощью команды:  
py -m pip install -r requirements.txt  
При этом у вас должен быть установлен менеджер пакетов pip.

Запуск бота выполняется из модуля main.py. Для запуска бота в консоли введите:  
python main.py

### Как пользоваться

#### default command:

**/start** - старт, команда для начала работы бота. Приветствует пользователя.

**/help** - помощь, выводит список доступных команд бота.

#### custom command:

**/most_value** - выводит самого дорогого футболиста команды на текущий момент.
Предварительно у пользователя запрашивается наименование (латиницей) интересующей 
его команды.

Запрос с параметрами:  
query_string = {"query": "Наименование команды", "domain": "com"}  
url: https://transfermarket.p.rapidapi.com/search

Пример ответа запроса (для экономии пространства ответ показан частично):  

```console
{"count":
    {"players": 0,
    "coaches": 0,
    "clubs": 6,
    "competitions": 0,
    "referees": 0},
    "clubs":
        [
            {"id": "985",
            "league": "GB1",
            "competitionID": "GB1",
            "competitionName": "Premier League",
            "name": "Manchester United",
            "logoImage": "https://tmssl.akamaized.net//images/wappen/medium/985.png?lm=1457975903"}
            
            {"id": "9251",
            "league": "GB21",
            "competitionID": "GB21",
            "competitionName": "Premier League 2",
            "name": "Manchester United U21",
```
После выполнения вышеуказанного запроса определяем id команды. По id выполняем второй 
запрос для получения данных по игрокам ранее указанной команды.  
query_string = {"id": "id", "saison_id": "2024", "domain": "com"}  
url: https://transfermarket.p.rapidapi.com/clubs/get-squad

Пример ответа запроса (для экономии пространства ответ показан частично):  

```console
{"squad":
    [
        0:
            {"height": "1,81",
            "foot": "rechts",
            "injury": "null",
            ...
            "marketvalue":
                {"value": 2500000,
                "currency": "€",
                "progression": "null"}
            }
    ]
}
```
Далее перебором определяем игрока с максимальной стоимостью и выводим его параметры:  
1. имя и фамилия;
2. цена;
3. возраст;
4. игровой номер.

**/awards** - выводит имя и фамилию игрока, получившего конкретную индивидуальную 
награду в конкретном году.  

Первоначально пользователю предлагается на выбор 3 типа индивидуальных наград 
футболистов: best fifa players, golden boot, clean sheets. После выбора типа 
индивидуальной награды делается соответствующий запрос к API.  

best fifa players:  
query_string = {"domain": "com"}  
url: https://transfermarket.p.rapidapi.com/statistic/list-best-fifa-players

golden boot:  
query_string = {"domain": "com"}  
url: https://transfermarket.p.rapidapi.com/statistic/list-golden-boot

clean sheets:  
query_string = {"domain": "com"}  
url: https://transfermarket.p.rapidapi.com/statistic/list-clean-sheets

Пример ответа запроса для best fifa players (для экономии пространства ответ 
показан частично):

```console
{
    "share":
        {
        ...
        }
    "player":
        [0: 
            {"year: 2021,
            "playerName": "R. Lewandowski",
            "firstName": "Robert",
            ...
            "marketValueAtThisTimeNumeral": "Mio."}
        1:
            {"year: 2020,
            ...
            "marketValueAtThisTimeNumeral": "Mio."}
        ]
}
```

Запрашиваем у пользователя год, в котором он хотел бы посмотреть, кто именно 
получил награду. По информации о годе ищем в полученных данных нужного футболиста.  
Выводим информацию по футболисту:  
1. имя и фамилия;
2. клуб;
3. возраст;
4. текущая стоимость.

### Этапы реализации бота
1. Выбор API и изучение документации.
2. Составление файла README.md.
3. Реализация вышеуказанных запросов и состояний (StatesGroup).
4. Реализация команды /history (SQL, Peewee).
5. Тестирование бота.
