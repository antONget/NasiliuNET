from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging


def keyboard_start_menu() -> InlineKeyboardMarkup:
    logging.info("keyboard_start_menu")
    button_1 = InlineKeyboardButton(text='Твоя история в группу поддержки',  callback_data=f'your_stories')
    button_2 = InlineKeyboardButton(text='Обратиться за помощью к Анастасии', callback_data=f'help_me')
    button_3 = InlineKeyboardButton(text='Получить контакты помощи', callback_data=f'contacts')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3]],)
    return keyboard


def keyboard_your_stories() -> InlineKeyboardMarkup:
    logging.info("keyboard_your_stories")
    button_1 = InlineKeyboardButton(text='Отправить историю',  callback_data=f'stories_send')
    button_2 = InlineKeyboardButton(text='Отмена', callback_data=f'BACK')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]],)
    return keyboard


def keyboard_back() -> InlineKeyboardMarkup:
    logging.info("keyboard_back")
    button_1 = InlineKeyboardButton(text='Отмена', callback_data=f'BACK')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]],)
    return keyboard


def keyboard_your_helpme() -> InlineKeyboardMarkup:
    logging.info("keyboard_your_stories")
    button_1 = InlineKeyboardButton(text='Отправить обращение',  callback_data=f'helpme_send')
    button_2 = InlineKeyboardButton(text='Отмена', callback_data=f'BACK')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]],)
    return keyboard


def keyboard_thanks() -> InlineKeyboardMarkup:
    logging.info("keyboard_thanks")
    button_1 = InlineKeyboardButton(text='Спасибо', callback_data=f'BACK')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]],)
    return keyboard