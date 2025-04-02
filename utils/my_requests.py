"""
Модуль содержит функцию, выполняющую запрос к API.
"""

from typing import Dict, Any

import requests


def api_request(method: str, params: Dict[str, Any]) -> Any:
    """
    Вернуть десереализированный ответ на запрос к API.

    :param method: добавочный путь запроса.
    :param params: параметры запроса.
    :return: десереализированный ответ.
    """

    url = 'https://transfermarket.p.rapidapi.com/{method}'.format(
        method=method
    )

    headers = {
        "x-rapidapi-key": "c6f160bdd2msh50ea8968eccfa92p120466jsncc76cc589eb8",
        "x-rapidapi-host": "transfermarket.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=params,
                                timeout=30)
        if response.status_code == requests.codes.ok:
            return response.json()
    except requests.exceptions.Timeout:
        return None
