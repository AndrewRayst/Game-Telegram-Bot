import json
import os
from typing import Dict, List, Union

import requests

from utils.exponential_backoff import exponential_backoff


T_game = Dict[str, Union[str, int, float]]


class API:
    __key = os.getenv('API_KEY')

    @exponential_backoff()
    def get(self) -> List[T_game] or any:
        url = "https://opencritic-api.p.rapidapi.com/game/popular"

        headers = {
            "X-RapidAPI-Key": self.__key,
            "X-RapidAPI-Host": "opencritic-api.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)

        if response.ok:
            return json.loads(response.text)

        return None
