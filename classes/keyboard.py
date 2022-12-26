from aiogram import Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from utils.emoji import demojize, emojize


class KeyBoard:
    def __init__(self, bot, dispatcher: Dispatcher) -> None:
        self.__bot = bot
        self.__dispatcher = dispatcher

    def get_main(self) -> ReplyKeyboardMarkup:
        self.remove()

        btn_game_rating = KeyboardButton(emojize('Game Rating'))
        btn_settings = KeyboardButton(emojize(':gear:'))
        btn_help = KeyboardButton('Help')
        btn_history = KeyboardButton(emojize('History'))

        return ReplyKeyboardMarkup(resize_keyboard=True)\
            .add(btn_game_rating).row(btn_settings, btn_history, btn_help)

    def get_settings(self) -> ReplyKeyboardMarkup:
        self.remove()

        btn_low = KeyboardButton('Low')
        btn_high = KeyboardButton('High')
        btn_custom = KeyboardButton('Custom')
        btn_back = KeyboardButton(emojize(':left_arrow:'))

        return ReplyKeyboardMarkup(resize_keyboard=True)\
            .row(btn_low, btn_high).add(btn_custom).add(btn_back)

    def remove(self) -> None:
        ReplyKeyboardRemove()

    def watch_keyboard(self) -> None:
        @self.__dispatcher.message_handler()
        async def keyboard_command(msg: types.Message) -> None:
            match demojize(msg.text):
                case ':gear:':
                    await msg.answer(self.__bot.settings(), reply_markup=self.get_settings())

                case ':left_arrow:':
                    new_msg = 'выбери команду ниже ' + emojize(':backhand_index_pointing_down:')
                    await msg.answer(text=new_msg, reply_markup=self.get_main())

                case 'Help':
                    await msg.answer(self.__bot.get_help())

                case 'History':
                    await msg.answer(self.__bot.get_history())

                case 'Game Rating':
                    await msg.answer(self.__bot.get_game_rating())

                case 'Low':
                    await msg.answer(self.__bot.set_low())

                case 'High':
                    await msg.answer(self.__bot.set_high())

                case 'Custom':
                    await msg.answer(self.__bot.set_custom())
