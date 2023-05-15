import config
from parsing import *
import duckdb
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class UserState(StatesGroup):
    CATEGORIES = State()
    SUBCATEGORIES = State()
    FOLOWWEEK = State()
    WAITSETTING = State()

class SubcategoryState(StatesGroup):
    CINEMA = State()
    CONCERT = State()
    THEATRE = State()
    SHOW = State()

class EventsState(StatesGroup):
    CATEGORY = State()
    SUBCATEGORY = State()
    PRINT_EVENT = State()

#Parsing()

def change_button_to_yes(i: int, j: int, keyboard: InlineKeyboardMarkup) -> None:
    text = keyboard.inline_keyboard[i][j].text
    callback_data = keyboard.inline_keyboard[i][j].callback_data[:-2]
    keyboard.inline_keyboard[i][j].text = '✅' + text
    keyboard.inline_keyboard[i][j].callback_data = callback_data + "YES"

def change_button_to_no(i: int, j: int, keyboard: InlineKeyboardMarkup) -> None:
    text = keyboard.inline_keyboard[i][j].text
    callback_data = keyboard.inline_keyboard[i][j].callback_data[:-3]
    keyboard.inline_keyboard[i][j].text = text[1::]
    keyboard.inline_keyboard[i][j].callback_data = callback_data + "NO"

########################################################################################################################
def keyboard_categories() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Кино', callback_data='cinema_NO'),
        InlineKeyboardButton('Концерты', callback_data='concert_NO'),
        InlineKeyboardButton('Театр', callback_data='theatre_NO'),
        InlineKeyboardButton('Шоу', callback_data='show_NO'),
        InlineKeyboardButton('Дальше➡️', callback_data='next')
    ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

@dp.message_handler(commands=['start'], state=None)
async def start(message: Message, state: FSMContext) -> None:
    await state.update_data(ID=message.from_user.id)
    await state.update_data(CATEGORIES=[])
    await state.update_data(SUBCATEGORIES=[])
    await UserState.CATEGORIES.set()

    msg1 = f'Привет, {message.from_user.first_name}!🙌\n' \
           f'Для начала предлагаю настроить бота для твоего удобства'
    sticker = 'CAACAgQAAxkBAAEIuJFkR6hI7xeNZE6F0DZix_p7geY8IAACawADzjkIDVlm6mN2kkvQLwQ'
    await bot.send_sticker(message.from_user.id, sticker=sticker)
    await message.answer(msg1)
    await select_categories(message, state)

@dp.message_handler(state=UserState.CATEGORIES)
async def select_categories(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    msg2 = 'Выбери категории, которые тебя интересуют'
    if 'USER_KEYBOARD_CATEGORIES' in user_data: keyboard = user_data['USER_KEYBOARD_CATEGORIES']
    else:
        keyboard = keyboard_categories()
        await state.update_data(USER_KEYBOARD_CATEGORIES=keyboard)
    await message.answer(msg2, reply_markup=keyboard)

@dp.callback_query_handler(filters.Text(endswith='_NO'), state=UserState.CATEGORIES)
async def add_category(callback: CallbackQuery, state: FSMContext) -> None:
    data = callback.data
    user_data = await state.get_data()
    keyboard = user_data['USER_KEYBOARD_CATEGORIES']
    categories = user_data['CATEGORIES']
    if data == 'cinema_NO':
        change_button_to_yes(0, 0, keyboard)
        categories.append('CINEMA')
    elif data == 'concert_NO':
        change_button_to_yes(0, 1, keyboard)
        categories.append('CONCERT')
    elif data == 'theatre_NO':
        change_button_to_yes(1, 0, keyboard)
        categories.append('THEATRE')
    elif data == 'show_NO':
        change_button_to_yes(1, 1, keyboard)
        categories.append('SHOW')

    await state.update_data(CATEGORIES=categories)
    await state.update_data(USER_KEYBOARD_CATEGORIES=keyboard)
    await callback.message.edit_text('Выбери категории, которые тебя интересуют', reply_markup=keyboard)

@dp.callback_query_handler(filters.Text(endswith='_YES'), state=UserState.CATEGORIES)
async def cancel_category(callback: CallbackQuery, state: FSMContext) -> None:
    data = callback.data
    user_data = await state.get_data()
    keyboard = user_data['USER_KEYBOARD_CATEGORIES']
    categories = user_data['CATEGORIES']
    if data == 'cinema_YES':
        change_button_to_no(0, 0, keyboard)
        categories.remove('CINEMA')
    elif data == 'concert_YES':
        change_button_to_no(0, 1, keyboard)
        categories.remove('CONCERT')
    elif data == 'theatre_YES':
        change_button_to_no(1, 0, keyboard)
        categories.remove('THEATRE')
    elif data == 'show_YES':
        change_button_to_no(1, 1, keyboard)
        categories.remove('SHOW')

    await state.update_data(CATEGORIES=categories)
    await state.update_data(USER_KEYBOARD_CATEGORIES=keyboard)
    await callback.message.edit_text('Выбери категории, которые тебя интересуют', reply_markup=keyboard)

########################################################################################################################
@dp.callback_query_handler(filters.Text('next'), state=UserState.CATEGORIES)
async def select_subcategories(callback: CallbackQuery, state: FSMContext) -> None:
    await UserState.SUBCATEGORIES.set()
    await select_cinema_subcategories(callback, state)

def keyboard_cinema_subcategories() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Боевик', callback_data='cinema_action_NO'),
        InlineKeyboardButton('Драма', callback_data='cinema_drama_NO'),
        InlineKeyboardButton('Комедия', callback_data='cinema_comedy_NO'),
        InlineKeyboardButton('Мелодрама', callback_data='cinema_romance_NO'),
        InlineKeyboardButton('Приключения', callback_data='cinema_adventure_NO'),
        InlineKeyboardButton('Триллер', callback_data='cinema_thriller_NO'),
        InlineKeyboardButton('Ужасы', callback_data='cinema_horror_NO'),
        InlineKeyboardButton('Фантастика', callback_data='cinema_fiction_NO'),
        InlineKeyboardButton('Мультфильмы', callback_data='cinema_cartoon_NO'),
    ]
    button_next = InlineKeyboardButton('Дальше➡️', callback_data='next')
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    keyboard.add(button_next)
    return keyboard

@dp.callback_query_handler(state=UserState.SUBCATEGORIES)
async def select_cinema_subcategories(callback: CallbackQuery, state: FSMContext):
    await SubcategoryState.CINEMA.set()
    user_data = await state.get_data()
    if 'CINEMA' in user_data['CATEGORIES']:
        if 'USER_KEYBOARD_CINEMA_SUBCATEGORIES' in user_data:
            keyboard = user_data['USER_KEYBOARD_CINEMA_SUBCATEGORIES']
        else:
            keyboard = keyboard_cinema_subcategories()
            await state.update_data(USER_KEYBOARD_CINEMA_SUBCATEGORIES=keyboard)
        await callback.message.answer("Ты выбрал категорию \"Кино\". Какие жанры кино ты любишь?", reply_markup=keyboard)
    else:
        await select_concert_subcategories(callback, state)
        print('Кино не выбрано')

@dp.callback_query_handler(filters.Text(endswith='_NO'), state=SubcategoryState.CINEMA)
async def add_category(callback: CallbackQuery, state: FSMContext) -> None:
    data = callback.data
    user_data = await state.get_data()
    keyboard = user_data['USER_KEYBOARD_CINEMA_SUBCATEGORIES']
    subcategories = user_data['SUBCATEGORIES']
    if data == 'cinema_action_NO':
        change_button_to_yes(0, 0, keyboard)
        subcategories.append('CINEMA_ACTION')
    elif data == 'cinema_drama_NO':
        change_button_to_yes(0, 1, keyboard)
        subcategories.append('CINEMA_DRAMA')
    elif data == 'cinema_comedy_NO':
        change_button_to_yes(1, 0, keyboard)
        subcategories.append('CINEMA_COMEDY')
    elif data == 'cinema_romance_NO':
        change_button_to_yes(1, 1, keyboard)
        subcategories.append('CINEMA_ROMANCE')
    elif data == 'cinema_adventure_NO':
        change_button_to_yes(2, 0, keyboard)
        subcategories.append('CINEMA_ADVENTURE')
    elif data == 'cinema_thriller_NO':
        change_button_to_yes(2, 1, keyboard)
        subcategories.append('CINEMA_THRILLER')
    elif data == 'cinema_horror_NO':
        change_button_to_yes(3, 0, keyboard)
        subcategories.append('CINEMA_HORROR')
    elif data == 'cinema_fiction_NO':
        change_button_to_yes(3, 1, keyboard)
        subcategories.append('CINEMA_FICTION')
    elif data == 'cinema_cartoon_NO':
        change_button_to_yes(4, 0, keyboard)
        subcategories.append('CINEMA_CARTOON')


    await state.update_data(SUBCATEGORIES=subcategories)
    await state.update_data(USER_KEYBOARD_CINEMA_SUBCATEGORIES=keyboard)
    await callback.message.edit_text("Ты выбрал категорию \"Кино\". Какие жанры кино ты любишь?", reply_markup=keyboard)

@dp.callback_query_handler(filters.Text(endswith='_YES'), state=SubcategoryState.CINEMA)
async def add_category(callback: CallbackQuery, state: FSMContext) -> None:
    data = callback.data
    user_data = await state.get_data()
    keyboard = user_data['USER_KEYBOARD_CINEMA_SUBCATEGORIES']
    subcategories = user_data['SUBCATEGORIES']
    if data == 'cinema_action_YES':
        change_button_to_no(0, 0, keyboard)
        subcategories.remove('CINEMA_ACTION')
    elif data == 'cinema_drama_YES':
        change_button_to_no(0, 1, keyboard)
        subcategories.remove('CINEMA_DRAMA')
    elif data == 'cinema_comedy_YES':
        change_button_to_no(1, 0, keyboard)
        subcategories.remove('CINEMA_COMEDY')
    elif data == 'cinema_romance_YES':
        change_button_to_no(1, 1, keyboard)
        subcategories.remove('CINEMA_ROMANCE')
    elif data == 'cinema_adventure_YES':
        change_button_to_no(2, 0, keyboard)
        subcategories.remove('CINEMA_ADVENTURE')
    elif data == 'cinema_thriller_YES':
        change_button_to_no(2, 1, keyboard)
        subcategories.remove('CINEMA_THRILLER')
    elif data == 'cinema_horror_YES':
        change_button_to_no(3, 0, keyboard)
        subcategories.remove('CINEMA_HORROR')
    elif data == 'cinema_fiction_YES':
        change_button_to_no(3, 1, keyboard)
        subcategories.remove('CINEMA_FICTION')
    elif data == 'cinema_cartoon_YES':
        change_button_to_no(4, 0, keyboard)
        subcategories.remove('CINEMA_CARTOON')

    await state.update_data(SUBCATEGORIES=subcategories)
    await state.update_data(USER_KEYBOARD_CINEMA_SUBCATEGORIES=keyboard)
    await callback.message.edit_text("Ты выбрал категорию \"Кино\". Какие жанры кино ты любишь?", reply_markup=keyboard)

########################################################################################################################
def keyboard_concert_subcategories() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Поп', callback_data='concert_pop_NO'),
        InlineKeyboardButton('Хип-хоп и рэп', callback_data='concert_hiphop_rap_NO'),
        InlineKeyboardButton('Рок', callback_data='concert_rock_NO'),
        InlineKeyboardButton('Металл', callback_data='concert_methal_NO'),
        InlineKeyboardButton('Классическая музыка', callback_data='concert_classicalmusic_NO')
    ]
    button_next = InlineKeyboardButton('Дальше➡️', callback_data='next')
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    keyboard.add(button_next)
    return keyboard

@dp.callback_query_handler(filters.Text('next'), state=SubcategoryState.CINEMA)
async def select_concert_subcategories(callback: CallbackQuery, state: FSMContext):
    await SubcategoryState.CONCERT.set()
    user_data = await state.get_data()
    if 'CONCERT' in user_data['CATEGORIES']:
        if 'USER_KEYBOARD_CONCERT_SUBCATEGORIES' in user_data:
            keyboard = user_data['USER_KEYBOARD_CONCERT_SUBCATEGORIES']
        else:
            keyboard = keyboard_concert_subcategories()
            await state.update_data(USER_KEYBOARD_CONCERT_SUBCATEGORIES=keyboard)
        await callback.message.answer("Ты выбрал категорию \"Концерты\". Какие жанры музыки ты любишь?", reply_markup=keyboard)
    else:
        await select_theatre_subcategories(callback, state)
        print('Концерты не выбрано')

@dp.callback_query_handler(filters.Text(endswith='_NO'), state=SubcategoryState.CONCERT)
async def add_category(callback: CallbackQuery, state: FSMContext) -> None:
    data = callback.data
    user_data = await state.get_data()
    keyboard = user_data['USER_KEYBOARD_CONCERT_SUBCATEGORIES']
    subcategories = user_data['SUBCATEGORIES']
    if data == 'concert_pop_NO':
        change_button_to_yes(0, 0, keyboard)
        subcategories.append('CONCERT_POP')
    elif data == 'concert_hiphop_rap_NO':
        change_button_to_yes(0, 1, keyboard)
        subcategories.append('CONCERT_HIPHOP_RAP')
    elif data == 'concert_rock_NO':
        change_button_to_yes(1, 0, keyboard)
        subcategories.append('CONCERT_ROCK')
    elif data == 'concert_methal_NO':
        change_button_to_yes(1, 1, keyboard)
        subcategories.append('CONCERT_METHAL')
    elif data == 'concert_classicalmusic_NO':
        change_button_to_yes(2, 0, keyboard)
        subcategories.append('CONCERT_CLASSICAL_MUSIC')


    await state.update_data(SUBCATEGORIES=subcategories)
    await state.update_data(USER_KEYBOARD_CONCERT_SUBCATEGORIES=keyboard)
    await callback.message.edit_text("Ты выбрал категорию \"Концерты\". Какие жанры музыки ты любишь?", reply_markup=keyboard)

@dp.callback_query_handler(filters.Text(endswith='_YES'), state=SubcategoryState.CONCERT)
async def add_category(callback: CallbackQuery, state: FSMContext) -> None:
    data = callback.data
    user_data = await state.get_data()
    keyboard = user_data['USER_KEYBOARD_CONCERT_SUBCATEGORIES']
    subcategories = user_data['SUBCATEGORIES']
    if data == 'concert_pop_YES':
        change_button_to_no(0, 0, keyboard)
        subcategories.remove('CONCERT_POP')
    elif data == 'concert_hiphop_rap_YES':
        change_button_to_no(0, 1, keyboard)
        subcategories.remove('CONCERT_HIPHOP_RAP')
    elif data == 'concert_rock_YES':
        change_button_to_no(1, 0, keyboard)
        subcategories.remove('CONCERT_ROCK')
    elif data == 'concert_methal_YES':
        change_button_to_no(1, 1, keyboard)
        subcategories.remove('CONCERT_METHAL')
    elif data == 'concert_classicalmusic_YES':
        change_button_to_no(2, 0, keyboard)
        subcategories.remove('CONCERT_CLASSICAL_MUSIC')


    await state.update_data(SUBCATEGORIES=subcategories)
    await state.update_data(USER_KEYBOARD_CONCERT_SUBCATEGORIES=keyboard)
    await callback.message.edit_text("Ты выбрал категорию \"Концерты\". Какие жанры музыки ты любишь?", reply_markup=keyboard)

########################################################################################################################
def keyboard_theatre_subcategories() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Комедия', callback_data='theatre_comedy_NO'),
        InlineKeyboardButton('Драма', callback_data='theatre_drama_NO'),
        InlineKeyboardButton('Моноспектакль', callback_data='theatre_monoperformance_NO'),
        InlineKeyboardButton('Мьюзикл', callback_data='theatre_musical_NO'),
    ]
    button_next = InlineKeyboardButton('Дальше➡️', callback_data='next')
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    keyboard.add(button_next)
    return keyboard

@dp.callback_query_handler(filters.Text('next'), state=SubcategoryState.CONCERT)
async def select_theatre_subcategories(callback: CallbackQuery, state: FSMContext):
    await SubcategoryState.THEATRE.set()
    user_data = await state.get_data()
    if 'THEATRE' in user_data['CATEGORIES']:
        if 'USER_KEYBOARD_THEATRE_SUBCATEGORIES' in user_data:
            keyboard = user_data['USER_KEYBOARD_THEATRE_SUBCATEGORIES']
        else:
            keyboard = keyboard_theatre_subcategories()
            await state.update_data(USER_KEYBOARD_THEATRE_SUBCATEGORIES=keyboard)
        await callback.message.answer("Ты выбрал категорию \"Театр\". Какие постановки ты любишь?", reply_markup=keyboard)
    else:
        await select_show_subcategories(callback, state)
        print('Театр не выбрано')

@dp.callback_query_handler(filters.Text(endswith='_NO'), state=SubcategoryState.THEATRE)
async def add_category(callback: CallbackQuery, state: FSMContext) -> None:
    data = callback.data
    user_data = await state.get_data()
    keyboard = user_data['USER_KEYBOARD_THEATRE_SUBCATEGORIES']
    subcategories = user_data['SUBCATEGORIES']
    if data == 'theatre_comedy_NO':
        change_button_to_yes(0, 0, keyboard)
        subcategories.append('THEATRE_COMEDY')
    elif data == 'theatre_drama_NO':
        change_button_to_yes(0, 1, keyboard)
        subcategories.append('THEATRE_DRAMA')
    elif data == 'theatre_monoperformance_NO':
        change_button_to_yes(1, 0, keyboard)
        subcategories.append('THEATRE_MONOPERFORMANCE')
    elif data == 'theatre_musical_NO':
        change_button_to_yes(1, 1, keyboard)
        subcategories.append('THEATRE_MUSICAL')


    await state.update_data(SUBCATEGORIES=subcategories)
    await state.update_data(USER_KEYBOARD_THEATRE_SUBCATEGORIES=keyboard)
    await callback.message.edit_text("Ты выбрал категорию \"Театр\". Какие постановки ты любишь?", reply_markup=keyboard)

@dp.callback_query_handler(filters.Text(endswith='_YES'), state=SubcategoryState.THEATRE)
async def add_category(callback: CallbackQuery, state: FSMContext) -> None:
    data = callback.data
    user_data = await state.get_data()
    keyboard = user_data['USER_KEYBOARD_THEATRE_SUBCATEGORIES']
    subcategories = user_data['SUBCATEGORIES']
    if data == 'theatre_comedy_YES':
        change_button_to_no(0, 0, keyboard)
        subcategories.remove('THEATRE_COMEDY')
    elif data == 'theatre_drama_YES':
        change_button_to_no(0, 1, keyboard)
        subcategories.remove('THEATRE_DRAMA')
    elif data == 'theatre_monoperformance_YES':
        change_button_to_no(1, 0, keyboard)
        subcategories.remove('THEATRE_MONOPERFORMANCE')
    elif data == 'theatre_musical_YES':
        change_button_to_no(1, 1, keyboard)
        subcategories.remove('THEATRE_MUSICAL')


    await state.update_data(SUBCATEGORIES=subcategories)
    await state.update_data(USER_KEYBOARD_THEATRE_SUBCATEGORIES=keyboard)
    await callback.message.edit_text("Ты выбрал категорию \"Театр\". Какие постановки ты любишь?", reply_markup=keyboard)

########################################################################################################################
def keyboard_show_subcategories() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Стендап', callback_data='show_standup_NO'),
        InlineKeyboardButton('Детям', callback_data='show_kids_NO'),
        InlineKeyboardButton('Без детей', callback_data='show_nonchildren_NO'),
    ]
    button_next = InlineKeyboardButton('Дальше➡️', callback_data='next')
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    keyboard.add(button_next)
    return keyboard

@dp.callback_query_handler(filters.Text('next'), state=SubcategoryState.THEATRE)
async def select_show_subcategories(callback: CallbackQuery, state: FSMContext):
    await SubcategoryState.SHOW.set()
    user_data = await state.get_data()
    if 'SHOW' in user_data['CATEGORIES']:
        if 'USER_KEYBOARD_SHOW_SUBCATEGORIES' in user_data:
            keyboard = user_data['USER_KEYBOARD_SHOW_SUBCATEGORIES']
        else:
            keyboard = keyboard_show_subcategories()
            await state.update_data(USER_KEYBOARD_SHOW_SUBCATEGORIES=keyboard)
        await callback.message.answer("Ты выбрал категорию \"Шоу\". Что тебя интересует?", reply_markup=keyboard)
    else:
        print('Шоу не выбрано')
        await select_followweek_subcategories(callback, state)

@dp.callback_query_handler(filters.Text(endswith='_NO'), state=SubcategoryState.SHOW)
async def add_category(callback: CallbackQuery, state: FSMContext) -> None:
    data = callback.data
    user_data = await state.get_data()
    keyboard = user_data['USER_KEYBOARD_SHOW_SUBCATEGORIES']
    subcategories = user_data['SUBCATEGORIES']
    if data == 'show_standup_NO':
        change_button_to_yes(0, 0, keyboard)
        subcategories.append('SHOW_STANDUP')
    elif data == 'show_kids_NO':
        change_button_to_yes(0, 1, keyboard)
        subcategories.append('SHOW_KIDS')
    elif data == 'show_nonchildren_NO':
        change_button_to_yes(1, 0, keyboard)
        subcategories.append('SHOW_NON_CHILDREN')


    await state.update_data(SUBCATEGORIES=subcategories)
    await state.update_data(USER_KEYBOARD_SHOW_SUBCATEGORIES=keyboard)
    await callback.message.edit_text("Ты выбрал категорию \"Шоу\". Что тебя интересует?", reply_markup=keyboard)

@dp.callback_query_handler(filters.Text(endswith='_YES'), state=SubcategoryState.SHOW)
async def add_category(callback: CallbackQuery, state: FSMContext) -> None:
    data = callback.data
    user_data = await state.get_data()
    keyboard = user_data['USER_KEYBOARD_SHOW_SUBCATEGORIES']
    subcategories = user_data['SUBCATEGORIES']
    if data == 'show_standup_YES':
        change_button_to_no(0, 0, keyboard)
        subcategories.remove('SHOW_STANDUP')
    elif data == 'show_kids_YES':
        change_button_to_no(0, 1, keyboard)
        subcategories.remove('SHOW_KIDS')
    elif data == 'show_nonchildren_YES':
        change_button_to_no(1, 0, keyboard)
        subcategories.remove('SHOW_NON_CHILDREN')


    await state.update_data(SUBCATEGORIES=subcategories)
    await state.update_data(USER_KEYBOARD_SHOW_SUBCATEGORIES=keyboard)
    await callback.message.edit_text("Ты выбрал категорию \"Шоу\". Что тебя интересует?", reply_markup=keyboard)

########################################################################################################################
def keyboard_followweek() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Да', callback_data='followweek_YES'),
        InlineKeyboardButton('Нет', callback_data='followweek_NO'),
    ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

@dp.callback_query_handler(filters.Text('next'), state=SubcategoryState.SHOW)
async def select_followweek_subcategories(callback: CallbackQuery, state: FSMContext):
    await UserState.FOLOWWEEK.set()
    await callback.message.answer("И последний вопрос: "
                                  "нужна ли тебе рассылка мероприятий по понедельникам?", reply_markup=keyboard_followweek())

@dp.callback_query_handler(filters.Text('followweek_NO'), state=UserState.FOLOWWEEK)
async def followweek_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Настройка окончена!')
    await state.update_data(FOLLOWWEEK=False)
    await UserState.WAITSETTING.set()

@dp.callback_query_handler(filters.Text('followweek_YES'), state=UserState.FOLOWWEEK)
async def followweek_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Настройка окончена!')
    await state.update_data(FOLLOWWEEK=True)
    await UserState.WAITSETTING.set()

########################################################################################################################



    # elif callback.data in ['CINEMA', 'CONCERT', 'THEATRE', 'SHOW']:
    #     if callback.data == 'CINEMA': EVENTS = duckdb.sql("SELECT * FROM 'eventsDB.parquet' WHERE category='CINEMA'").fetchall()
    #     elif callback.data == 'CONCERT': EVENTS = duckdb.sql("SELECT * FROM 'eventsDB.parquet' WHERE category='CONCERT'").fetchall()
    #     elif callback.data == 'THEATRE': EVENTS = duckdb.sql("SELECT * FROM 'eventsDB.parquet' WHERE category='THEATRE'").fetchall()
    #     elif callback.data == 'SHOW': EVENTS = duckdb.sql("SELECT * FROM 'eventsDB.parquet' WHERE category='SHOW'").fetchall()
    #
    #     #не работает, так как колбэк переносится в двойных кавычках, а sql такого не понимать
    #     #EVENTS = duckdb.sql(f"SELECT * FROM 'events_file.parquet' WHERE category={callback.data}").fetchall()
    #
    #
    #     length = len(EVENTS)
    #     position = 0
    #
    #     #добавить проверку есть ли место или время
    #     await callback.message.bot.send_photo(chat_id=callback.message.chat.id, photo=EVENTS[position][6],
    #                                           caption=f'{EVENTS[position][3]}\n'
    #                                                   f'Когда: {EVENTS[position][5]}\n'
    #                                                   f'Где: {EVENTS[position][4]}\n'
    #                                                   f'Ссылка на покупку: {EVENTS[position][7]}',
    #                                           reply_markup=markup_next)
    #     position += 1
    #     await bot.answer_callback_query(callback.id)
    #
    # elif callback.data == 'NEXT_EVENT':
    #     if position == length:
    #         await callback.message.answer('Конец(')
    #         EVENTS = None
    #         position = None
    #         length = None
    #     else:
    #         await callback.message.bot.send_photo(chat_id=callback.message.chat.id, photo=EVENTS[position][6],
    #                                               caption=f'{EVENTS[position][3]}\n'
    #                                                       f'Когда: {EVENTS[position][5]}\n'
    #                                                       f'Где: {EVENTS[position][4]}\n'
    #                                                       f'Ссылка на покупку: {EVENTS[position][7]}',
    #                                               reply_markup=markup_next)
    #
    #         position += 1
    # else:
    #     await callback.answer()



########################################################################################################################

@dp.message_handler(commands=['info'], state=UserState.WAITSETTING)
async def info(message: types.Message):
    await message.answer('EventsNN - это бот для поиска мероприятий в Нижнем Новгороде. '
                         'С помощью него вы с легкостью найдете мероприятие на свой вкус.\n\n'
                         'Доступные команды:\n'
                         '/events - просмотр мероприятий по категориям\n'
                         '/settings - настроить подписку на категории\n'
                         '/info - информация о боте и все команды')


########################################################################################################################
def keyboard_event_categories() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Кино', callback_data='cinema'),
        InlineKeyboardButton('Концерты', callback_data='concert'),
        InlineKeyboardButton('Театр', callback_data='theatre'),
        InlineKeyboardButton('Шоу', callback_data='show'),
        InlineKeyboardButton('Все', callback_data='all')
    ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

@dp.message_handler(commands=['events'], state=UserState.WAITSETTING)
async def events(message: types.Message):
    await EventsState.CATEGORY.set()
    await message.answer('Какая категория тебя интересует?', reply_markup=keyboard_event_categories())

@dp.callback_query_handler(filters.Text('cinema'), state=EventsState.CATEGORY)
async def cinema_category(callback: CallbackQuery, state: FSMContext):
    await EventsState.SUBCATEGORY.set()
    await callback.message.answer('Здесь будут выводиться подкатегории кино')

@dp.callback_query_handler(filters.Text('concert'), state=EventsState.CATEGORY)
async def concert_category(callback: CallbackQuery, state: FSMContext):
    await EventsState.SUBCATEGORY.set()
    await callback.message.answer('Здесь будут выводиться подкатегории концертов')

@dp.callback_query_handler(filters.Text('theatre'), state=EventsState.CATEGORY)
async def theatre_category(callback: CallbackQuery, state: FSMContext):
    await EventsState.SUBCATEGORY.set()
    await callback.message.answer('Здесь будут выводиться подкатегории театров')

@dp.callback_query_handler(filters.Text('show'), state=EventsState.CATEGORY)
async def show_category(callback: CallbackQuery, state: FSMContext):
    await EventsState.SUBCATEGORY.set()
    await callback.message.answer('Здесь будут выводиться подкатегории шоу')

@dp.callback_query_handler(filters.Text('all'), state=EventsState.CATEGORY)
async def all_category(callback: CallbackQuery, state: FSMContext):
    await EventsState.PRINT_EVENT.set()
    await callback.message.answer('Здесь будут выводиться все мероприятия')

########################################################################################################################

@dp.message_handler(commands=['settings'], state=UserState.WAITSETTING)
async def settings(message: types.Message, state: FSMContext):
    await UserState.CATEGORIES.set()
    await select_categories(message, state)


executor.start_polling(dp)
