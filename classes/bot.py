import os

from aiogram import Bot as AIOBot, Dispatcher, executor, types


class Bot:
    def __init__(self) -> None:
        self.__aioBot = AIOBot(token=os.getenv('BOT_TOKEN'))
        self.__dispatcher = Dispatcher(self.__aioBot)

    def run(self) -> None:

        @self.__dispatcher.message_handler()
        async def echo_send(msg: types.Message) -> None:
            match msg.text:
                case '':
                    await msg.answer('')

                case _:
                    await msg.answer('Простите, но данная команда не существует.')

        executor.start_polling(self.__dispatcher, skip_updates=True)
