import json
from typing import List, Tuple, Union

from classes.models import DB, History, Settings


T_limit = Union[int, float]


class DataBase:
    __db = DB
    __history = History
    __settings = Settings

    def __init__(self):
        with self.__db:
            self.__db.create_tables([self.__history, self.__settings])

    def write_history(self, user_id: int, query_name: str):
        history: List[str] = self.get_history(user_id)
        history = [query_name] + history

        if len(history) > 10:
            history = history[:10]

        data = json.dumps(history)

        self.__history\
            .update(query_history=data)\
            .where(self.__history.user_id == user_id)\
            .execute()

    def get_history(self, user_id: int) -> List[str]:
        data = self.__history.get_or_none(self.__history.user_id == user_id)

        if data:
            return json.loads(data.query_history)

        else:
            self.__history.create(user_id=user_id, query_history='[]')

        return []

    def set_low(self, user_id: int, limit: T_limit):
        self.__settings\
            .update(low=limit)\
            .where(self.__settings.user_id == user_id)\
            .execute()

    def set_high(self, user_id: int, limit: T_limit):
        self.__settings \
            .update(high=limit) \
            .where(self.__settings.user_id == user_id) \
            .execute()

    def set_custom(self, user_id: int, low_limit: T_limit, high_limit: T_limit):
        self.__settings \
            .update(low=low_limit, high=high_limit) \
            .where(self.__settings.user_id == user_id) \
            .execute()

    def get_limits(self, user_id: int) -> Tuple[float, float]:
        structure = self.__settings.get_or_none(self.__settings.user_id == user_id)

        if structure is None:
            self.__settings.create(user_id=user_id, low=0.0, high=100.0)
            return 0.0, 100.0

        return structure.low, structure.high
