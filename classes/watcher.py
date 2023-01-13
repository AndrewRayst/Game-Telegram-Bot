from aiogram import types
from aiogram.dispatcher import FSMContext

from utils.emoji import demojize, emojize


class Watcher:
    def __init__(self, bot):
        self.bot = bot

    def watch_commands(self):
        @self.bot.dispatcher.message_handler(commands=self.bot.bot_commands)
        async def command(msg: types.Message) -> None:
            user_id = msg.from_user.id

            match msg.text:
                case '/start':
                    await msg.answer(self.bot.start(user_id), reply_markup=self.bot.keyboard.get_main())

                case '/help':
                    await msg.answer(self.bot.get_help(user_id))
                case '/low':
                    await msg.answer('Введите минимальный рейтинг:')
                    await self.bot.BotStates.low.set()
                case '/high':
                    await msg.answer(self.bot.set_high(user_id))
                case '/custom':
                    await msg.answer('Введите минимальный рейтинг:')
                    await self.bot.states.Custom.low.set()
                case '/game_rating':
                    await msg.answer(self.bot.get_game_rating(user_id))
                case '/history':
                    await msg.answer(self.bot.get_history(user_id))
                case '/settings':
                    new_msg = 'Настройки ' + emojize(':backhand_index_pointing_down:')
                    await msg.answer(new_msg, reply_markup=self.bot.keyboard.get_settings())

                case _:
                    await msg.answer('Простите, но данная команда не существует.')

    def watch_keyboard(self) -> None:
        @self.bot.dispatcher.message_handler()
        async def keyboard_command(msg: types.Message) -> None:
            user_id = msg.from_user.id

            match demojize(msg.text):
                case ':gear:':
                    new_msg = 'Настройки ' + emojize(':backhand_index_pointing_down:')
                    await msg.answer(new_msg, reply_markup=self.bot.keyboard.get_settings())

                case ':left_arrow:':
                    new_msg = 'Выбери команду ниже ' + emojize(':backhand_index_pointing_down:')
                    await msg.answer(text=new_msg, reply_markup=self.bot.keyboard.get_main())

                case 'Help':
                    await msg.answer(self.bot.get_help(user_id))

                case 'History':
                    await msg.answer(self.bot.get_history(user_id))

                case 'Game Rating':
                    await msg.answer(self.bot.get_game_rating(user_id))

                case 'Low':
                    await msg.answer('Введите минимальный рейтинг:')
                    await self.bot.states.low.set()

                case 'High':
                    await msg.answer('Введите максимальный рейтинг:')
                    await self.bot.states.high.set()

                case 'Custom':
                    await msg.answer('Введите минимальный рейтинг:')
                    await self.bot.states.Custom.low.set()

    @staticmethod
    async def get_limit(msg: types.Message) -> float:
        try:
            answer = round(float(msg.text), 2)

            if (answer < 0) or (answer > 100):
                raise ValueError

            return answer

        except ValueError:
            await msg.answer('Введено некорректное значение')

    def watch_low_cb(self):
        @self.bot.dispatcher.message_handler(content_types='text', state=self.bot.states.low)
        async def command(msg: types.Message, state: FSMContext) -> None:
            limit = await self.get_limit(msg=msg)

            if isinstance(limit, int) or isinstance(limit, float):
                await msg.answer(self.bot.set_low(msg.from_user.id, limit=limit))

            await state.finish()

    def watch_high_cb(self):
        @self.bot.dispatcher.message_handler(content_types='text', state=self.bot.states.high)
        async def command(msg: types.Message, state: FSMContext) -> None:
            limit = await self.get_limit(msg=msg)

            if isinstance(limit, int) or isinstance(limit, float):
                await msg.answer(self.bot.set_high(msg.from_user.id, limit=limit))

            await state.finish()

    def watch_custom_cb(self):
        @self.bot.dispatcher.message_handler(content_types='text', state=self.bot.states.Custom.low)
        async def command_low(msg: types.Message, state: FSMContext) -> None:
            limit = await self.get_limit(msg=msg)

            if isinstance(limit, float) or isinstance(limit, int):
                async with state.proxy() as data:
                    data['low'] = limit

            else:
                await self.bot.states.Custom.low.set()
                return

            await self.bot.states.Custom.next()
            await msg.answer('Введите максимальный рейтинг:')

        @self.bot.dispatcher.message_handler(content_types='text', state=self.bot.states.Custom.high)
        async def command_high(msg: types.Message, state: FSMContext) -> None:
            limit = await self.get_limit(msg=msg)

            if isinstance(limit, float) or isinstance(limit, int):
                async with state.proxy() as data:
                    data['high'] = limit

            else:
                await self.bot.states.Custom.high.set()
                return

            async with state.proxy() as data:
                self.bot.set_custom(
                    user_id=msg.from_user.id,
                    limit_low=data['low'],
                    limit_high=data['high']
                )

            await state.finish()
            await msg.answer('Изменения приняты')

    def run(self):
        self.watch_commands()
        self.watch_keyboard()
        self.watch_low_cb()
        self.watch_high_cb()
        self.watch_custom_cb()
