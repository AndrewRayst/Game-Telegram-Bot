from aiogram import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove

from utils.emoji import emojize


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

    @staticmethod
    def get_rating_keyboard() -> InlineKeyboardMarkup:
        btn_prev = InlineKeyboardButton(text='<-', callback_data='rating_prev')
        btn_next = InlineKeyboardButton(text='->', callback_data='rating_next')

        return InlineKeyboardMarkup(row_width=2).row(btn_prev, btn_next)

    @staticmethod
    def remove() -> None:
        ReplyKeyboardRemove()
