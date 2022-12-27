import os
from typing import List

from aiogram import Bot as AIOBot, Dispatcher, executor, types

from classes.api import API
from classes.keyboard import KeyBoard

from utils.emoji import emojize


class Bot:
    __bot_commands: List[str] = [
        'start', 'help', 'low',
        'high', 'custom', 'history',
        'game_rating', 'settings'
    ]

    def __init__(self) -> None:
        self.__aioBot = AIOBot(token=os.getenv('BOT_TOKEN'))
        self.__dispatcher = Dispatcher(self.__aioBot)
        self.__keyboard = KeyBoard(self, self.__dispatcher)
        self.__api = API()

    def start(self) -> str:
        self.write_history('start')
        return 'Приветствую!!! Я могу показать тебе рейтинг игр. ' \
               'Только выбери команду ниже ' + emojize(':backhand_index_pointing_down:')

    def get_help(self) -> str:
        self.write_history('help')
        return '/game_rating - рейтинг игр.\n' \
               '/history - история команд\n' \
               '/low - установить минимальный рейтинг.\n' \
               '/high - установить максимальный рейтинг.\n' \
               '/custom - установить диапазон рейтинга.'

    def set_low(self) -> str:
        self.write_history('low')
        return 'low'

    def set_high(self) -> str:
        self.write_history('high')
        return 'high'

    def set_custom(self) -> str:
        self.write_history('custom')
        return 'custom'

    def get_history(self) -> str:
        return 'history'

    def write_history(self, command: str) -> None:
        pass

    def settings(self) -> str:
        return 'settings'

    def get_game_rating(self) -> str:
        self.write_history('game_rating')
        data = self.__api.get()

        if data:
            print(list([(i_item['name'], i_item['topCriticScore']) for i_item in data]))
            return 'rating'

        return 'Ошибка соединения'

    def watch_command(self) -> None:
        @self.__dispatcher.message_handler(commands=self.__bot_commands)
        async def command(msg: types.Message) -> None:
            match msg.text:
                case '/start':
                    await msg.answer(self.start(), reply_markup=self.__keyboard.get_main())

                case '/help': await msg.answer(self.get_help())
                case '/low': await msg.answer(self.set_low())
                case '/high': await msg.answer(self.set_high())
                case '/custom': await msg.answer(self.set_custom())
                case '/game_rating': await msg.answer(self.get_game_rating())
                case '/history': await msg.answer(self.get_history())
                case '/settings':
                    await msg.answer(self.settings(), reply_markup=self.__keyboard.get_settings())

                case _: await msg.answer('Простите, но данная команда не существует.')

    def run(self) -> None:
        async def on_startup(_: any) -> None:
            print('Бот включился')

        self.watch_command()
        self.__keyboard.watch_keyboard()

        executor.start_polling(
            self.__dispatcher,
            skip_updates=True,
            on_startup=on_startup
        )
