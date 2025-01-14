from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from keyboards import user_keyboards as kb

from config_data.config import Config, load_config
from utils.error_handling import error_handler
from utils.send_admins import send_message_admins


import logging

router = Router()
# Загружаем конфиг в переменную config
config: Config = load_config()


class User(StatesGroup):
    stories = State()
    helpme = State()


@router.message(CommandStart())
@error_handler
async def process_start_command_user(message: Message) -> None:
    """
    Пользовательский режим запускается если, пользователь ввел команду /start
     или если администратор ввел команду /user
    1. Добавляем пользователя в БД если его еще нет в ней
    :param message:
    :return:
    """
    logging.info(f'process_start_command_user: {message.chat.id}')
    try:
        await message.edit_text(text=f'Здравствуй! Ты в Боте Поддержки Анастасии Даниленко ❤️\n'
                                     f'Спасибо, что делишься со мной. Я готова и хочу помочь всем детям и уже '
                                     f'выросшим жертвам насилия.\n'
                                     f'Не бойся, если ты не захочешь, то этого не увидит'
                                     f' никто кроме меня.'
                                     f' Ниже выбери, что именно нужно сделать:',
                                reply_markup=kb.keyboard_start_menu())
    except:
        await message.answer(text=f'Здравствуй! Ты в БотеПоддержки Анастасии Даниленко ❤️\n'
                                  f'Спасибо, что делишься со мной. Я готова и хочу помочь всем детям и'
                                  f' уже выросшим жертвам'
                                  f' насилия.\n'
                                  f'Не бойся, если ты не захочешь, то этого не увидит никто кроме меня.'
                                  f' Ниже выбери, что именно нужно сделать:',
                             reply_markup=kb.keyboard_start_menu())


@router.callback_query(F.data == 'your_stories')
@error_handler
async def process_your_stories(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'process_your_stories: {callback.message.chat.id}')
    await callback.message.edit_text(text=f'Распиши свою историю так,'
                                          f' как хочешь чтобы её увидели другие участники группы.\n'
                                          f'Не бойся, в группе тебя не осудят и будут к тебе добры...\n'
                                          f'После отправки я получу это сообщение и отправлю в группу анонимно.'
                                          f' Имя свое ты откроешь только если захочешь этого ❤️',
                                     reply_markup=kb.keyboard_back())
    await state.update_data(stories='')
    await state.set_state(User.stories)


@router.message(F.text, StateFilter(User.stories))
@error_handler
async def answer_your_stories(message: Message, bot: Bot, state: FSMContext) -> None:
    logging.info(f'answer_your_stories: {message.chat.id}')
    try:
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id-1)
    except:
        pass
    await message.answer(text=f'Отлично, отправить?',
                         reply_markup=kb.keyboard_your_stories())
    data = await state.get_data()
    stories = data['stories']
    stories += message.html_text
    await state.update_data(stories=stories)
    await state.set_state(state=None)


@router.callback_query(F.data == 'BACK')
@error_handler
async def process_question(callback: CallbackQuery) -> None:
    logging.info(f'process_question: {callback.message.chat.id}')
    await process_start_command_user(message=callback.message)


@router.callback_query(F.data == 'stories_send')
@error_handler
async def process_stories_send(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    logging.info(f'process_stories_send: {callback.message.chat.id}')
    data = await state.get_data()
    stories = data['stories']
    if len(stories) > 4090:
        text = f'Получена история от @{callback.from_user.username}/{callback.from_user.id}\n\n'
        for stor_ in stories[::4090]:
            text += stor_
            await send_message_admins(bot=bot, text=text)
            text = ''
    else:
        text = f'Получена история от @{callback.from_user.username}/{callback.from_user.id}\n\n' + stories
        await send_message_admins(bot=bot, text=text)
    await callback.message.answer(text=f'Вот ссылка на группу, где скоро опубликую твою историю.'
                                       f' Там ты можешь отреагировать на истории других людей в похожих ситуациях.'
                                       f' Спасибо за доверие ❤️\n\n'
                                       f'https://t.me/+CX0q8OcMy0ZlNjIy',
                                  reply_markup=kb.keyboard_start_menu())


@router.callback_query(F.data == 'help_me')
@error_handler
async def process_help_me(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'process_help_me: {callback.message.chat.id}')
    await callback.message.edit_text(text=f'Распиши, пожалуйста, свою историю очень подробно. Это увижу только я.'
                                          f' Важные моменты:\n'
                                          f'1. В каком ты городе?\n'
                                          f'2. Сколько тебе лет сейчас?\n'
                                          f'3. Сколько лет было на момент совершения первого эпизода насилия'
                                          f' и последнего?\n'
                                          f'4. Какая степень опасности сейчас тебе грозит?\n'
                                          f'5. Способы связи с тобой (номер телефона, страница в ВК и тд)\n'
                                          f'Мне важна максимальная честность ❤️️',
                                     reply_markup=kb.keyboard_back())
    await state.update_data(helpme='')
    await state.set_state(User.helpme)


@router.message(F.text, StateFilter(User.helpme))
@error_handler
async def answer_helpme(message: Message, bot: Bot, state: FSMContext) -> None:
    logging.info(f'answer_helpme: {message.chat.id}')
    try:
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id-1)
    except:
        pass
    await message.answer(text=f'Отлично, отправить?',
                         reply_markup=kb.keyboard_your_helpme())

    data = await state.get_data()
    helpme = data['helpme']
    helpme += message.html_text
    await state.update_data(helpme=helpme)
    await state.set_state(state=None)


@router.callback_query(F.data == 'helpme_send')
@error_handler
async def process_stories_send(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    logging.info(f'process_stories_send: {callback.message.chat.id}')
    data = await state.get_data()
    helpme = data['helpme']
    if len(helpme) > 4090:
        text = f'Получена жалоба от @{callback.from_user.username}/{callback.from_user.id}\n\n'
        for help_ in helpme[::4090]:
            text += help_
            await send_message_admins(bot=bot, text=text)
            text = ''
    else:
        text = f'Получена жалоба от @{callback.from_user.username}/{callback.from_user.id}\n\n' + helpme
        await send_message_admins(bot=bot, text=text)
    await callback.message.answer(text=f'Я получила твое обращение, я постараюсь среагировать в ближайшее время!'
                                       f' Спасибо за доверие ❤️',
                                  reply_markup=kb.keyboard_start_menu())


@router.callback_query(F.data == 'contacts')
@error_handler
async def process_contacts(callback: CallbackQuery) -> None:
    logging.info(f'process_contacts: {callback.message.chat.id}')
    await callback.message.answer(text=f'☔️ Куда обратиться за помощью:\n\n'
                                       f'<a href="https://nasiliu.net"><b>Насилию.нет</b></a>\n\n'
                                       f'<a href="https://verimtebe.ru/consultations"><b>ТЕБЕ ПОВЕРЯТ</b></a>\n\n'
                                       f'<a href="https://crisiscenter.ru"><b>ИНГО кризисный центр для женщин</b></a>\n\n'
                                       f'💫  Запрос к начинающим терапевтам по минимальной цене через личные сообщения'
                                       f' <a href="https://vk.com/idnatali1811">Наталье</a>\n\n'
                                       f'💫  <a href="https://vk.com/topic-212684860_49313719">'
                                       f'Психолог, гештальт-терапевт, платно</a>\n\n',
                                  reply_markup=kb.keyboard_thanks())
    await callback.answer()
