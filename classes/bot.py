from typing import Dict, List, Union

from aiogram import Bot as AIOBot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN

from classes.api import API
from classes.data_base import DataBase
from classes.keyboard import KeyBoard
from classes.rating import Rating
from classes.states import States
from classes.watcher import Watcher

from utils.emoji import emojize


T_limit = int or float


class Bot:
    bot_commands: List[str] = [
        'start', 'help', 'low',
        'high', 'custom', 'history',
        'game_rating', 'settings'
    ]

    users_ratings: Dict[int, Rating] = dict()

    states = States

    def __init__(self) -> None:
        storage = MemoryStorage()

        self.__aioBot = AIOBot(token=BOT_TOKEN)
        self.dispatcher = Dispatcher(self.__aioBot, storage=storage)
        self.keyboard = KeyBoard(self, self.dispatcher)
        self.watcher = Watcher(self)
        self.__api = API()
        self.__db = DataBase()

    def start(self, user_id: int) -> str:
        self.__db.write_history(user_id=user_id, query_name='start')
        return 'Приветствую!!! Я могу показать тебе рейтинг игр. ' \
               'Только выбери команду ниже ' + emojize(':backhand_index_pointing_down:')

    def get_help(self, user_id: int) -> str:
        self.__db.write_history(user_id=user_id, query_name='help')
        return '/game_rating - рейтинг игр.\n' \
               '/history - история команд\n' \
               '/low - установить минимальный рейтинг.\n' \
               '/high - установить максимальный рейтинг.\n' \
               '/custom - установить диапазон рейтинга.'

    def set_custom(self, user_id: int, limit_low: T_limit, limit_high: T_limit) -> None:
        self.__db.write_history(user_id=user_id, query_name='custom')
        self.__db.set_custom(user_id=user_id, low_limit=limit_low, high_limit=limit_high)

    def set_low(self, user_id: int, limit: T_limit) -> str:
        self.__db.write_history(user_id=user_id, query_name='low')
        self.__db.set_low(user_id=user_id, limit=limit)
        return 'Изменения приняты'

    def set_high(self, user_id: int, limit: T_limit) -> str:
        self.__db.write_history(user_id=user_id, query_name='high')
        self.__db.set_high(user_id=user_id, limit=limit)
        return 'Изменения приняты'

    def get_history(self, user_id: int) -> str:
        history = [
            i_command.replace('_', ' ')
            for i_command in self.__db.get_history(user_id)
        ]

        return '<b>История команд:</b>\n(New)\n\t\t· ' + '\n\t\t· '.join(history) + '\n(Old)'

    def get_game_rating(self, user_id: int) -> Union[None, str]:
        def check_rating(item: any) -> bool:
            try:
                rating = int(item['topCriticScore'])

                if (rating < low_limit) or (rating > high_limit):
                    return False

                return True

            except ValueError:
                return False

        self.__db.write_history(user_id=user_id, query_name='game_rating')
        data = self.__api.get()

        low_limit, high_limit = self.__db.get_limits(user_id)

        if data:
            data = list(filter(check_rating, data))

            if not data:
                print(data)
                return 'Игр с данным рейтингом нет'

            data = sorted(data, key=lambda item: item['topCriticScore'], reverse=True)

            for i_item in data:
                i_item['topCriticScore'] = round(i_item['topCriticScore'], 2)

            self.users_ratings[user_id] = Rating(arr=data)

        else:
            return 'Ошибка соединения, попробуйте снова'

    def run(self) -> None:
        async def on_startup(_: any) -> None:
            print('Бот включился')

        self.watcher.run()

        executor.start_polling(
            self.dispatcher,
            skip_updates=True,
            on_startup=on_startup
        )
