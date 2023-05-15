from config import *

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class UserState(StatesGroup):
    CATEGORIES = State()
    SUBCATEGORIES = State()
    FOLOWWEEK = State()
    WAIT = State()

class SubcategoryState(StatesGroup):
    CINEMA = State()
    CONCERT = State()
    THEATRE = State()
    SHOW = State()

class EventsState(StatesGroup):
    CATEGORY = State()
    SUBCATEGORY = State()
    PRINT_EVENT = State()


# Parsing()
########################################################################################################################
@dp.message_handler(commands=['start'], state=None)
async def start(message: Message, state: FSMContext) -> None:
    await state.update_data(ID=message.from_user.id)
    await state.update_data(CATEGORIES=[])
    await state.update_data(SUBCATEGORIES=[])
    await UserState.CATEGORIES.set()

    await bot.send_sticker(message.from_user.id,
                           sticker='CAACAgQAAxkBAAEIuJFkR6hI7xeNZE6F0DZix_p7geY8IAACawADzjkIDVlm6mN2kkvQLwQ')
    await message.answer(f'Привет, {message.from_user.first_name}!🙌\n'
                         f'Для начала предлагаю настроить бота для твоего удобства')
    await select_categories(message, state)

########################################################################################################################
# настройка подписки
@dp.message_handler(state=UserState.CATEGORIES)
async def select_categories(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    msg2 = 'Выбери категории, которые тебя интересуют'
    if 'USER_KEYBOARD_CATEGORIES' in user_data:
        keyboard = user_data['USER_KEYBOARD_CATEGORIES']
    else:
        keyboard = keyboard_setting_categories()
        await state.update_data(USER_KEYBOARD_CATEGORIES=keyboard)
    await message.answer(msg2, reply_markup=keyboard)

@dp.callback_query_handler(filters.Text('cancel'), state=UserState.CATEGORIES)
async def cancel_setting(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        'Вы пропустили настройку подписки! Вы можете вернуться к этому позже командой /settings')
    await UserState.WAIT.set()
    await callback.answer()

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
    await callback.answer()

@dp.callback_query_handler(filters.Text(endswith='_YES'), state=UserState.CATEGORIES)
async def delete_category(callback: CallbackQuery, state: FSMContext) -> None:
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
    await callback.answer()

@dp.callback_query_handler(filters.Text('next'), state=UserState.CATEGORIES)
async def select_subcategories(callback: CallbackQuery, state: FSMContext) -> None:
    await UserState.SUBCATEGORIES.set()
    await select_cinema_subcategories(callback, state)
    await callback.answer()

#-----------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(state=UserState.SUBCATEGORIES)
async def select_cinema_subcategories(callback: CallbackQuery, state: FSMContext):
    await SubcategoryState.CINEMA.set()
    user_data = await state.get_data()
    if 'CINEMA' in user_data['CATEGORIES']:
        if 'USER_KEYBOARD_CINEMA_SUBCATEGORIES' in user_data:
            keyboard = user_data['USER_KEYBOARD_CINEMA_SUBCATEGORIES']
        else:
            keyboard = keyboard_setting_subcategories_cinema()
            await state.update_data(USER_KEYBOARD_CINEMA_SUBCATEGORIES=keyboard)
        await callback.message.answer("Ты выбрал категорию \"Кино\". Какие жанры кино ты любишь?",
                                      reply_markup=keyboard)
    else:
        await select_concert_subcategories(callback, state)
        print('Кино не выбрано')
    await callback.answer()

@dp.callback_query_handler(filters.Text(endswith='_NO'), state=SubcategoryState.CINEMA)
async def add_cinema_subcategory(callback: CallbackQuery, state: FSMContext) -> None:
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
    await callback.answer()

@dp.callback_query_handler(filters.Text(endswith='_YES'), state=SubcategoryState.CINEMA)
async def delete_cinema_subcategory(callback: CallbackQuery, state: FSMContext) -> None:
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
    await callback.answer()

#-----------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(filters.Text('next'), state=SubcategoryState.CINEMA)
async def select_concert_subcategories(callback: CallbackQuery, state: FSMContext):
    await SubcategoryState.CONCERT.set()
    user_data = await state.get_data()
    if 'CONCERT' in user_data['CATEGORIES']:
        if 'USER_KEYBOARD_CONCERT_SUBCATEGORIES' in user_data:
            keyboard = user_data['USER_KEYBOARD_CONCERT_SUBCATEGORIES']
        else:
            keyboard = keyboard_setting_subcategories_concert()
            await state.update_data(USER_KEYBOARD_CONCERT_SUBCATEGORIES=keyboard)
        await callback.message.answer("Ты выбрал категорию \"Концерты\". Какие жанры музыки ты любишь?",
                                      reply_markup=keyboard)
    else:
        await select_theatre_subcategories(callback, state)
        print('Концерты не выбрано')
    await callback.answer()


@dp.callback_query_handler(filters.Text(endswith='_NO'), state=SubcategoryState.CONCERT)
async def add_concert_subcategory(callback: CallbackQuery, state: FSMContext) -> None:
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
    await callback.message.edit_text("Ты выбрал категорию \"Концерты\". Какие жанры музыки ты любишь?",
                                     reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(filters.Text(endswith='_YES'), state=SubcategoryState.CONCERT)
async def delete_concert_subcategory(callback: CallbackQuery, state: FSMContext) -> None:
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
    await callback.message.edit_text("Ты выбрал категорию \"Концерты\". Какие жанры музыки ты любишь?",
                                     reply_markup=keyboard)
    await callback.answer()

#-----------------------------------------------------------------------------------------------------------------------

@dp.callback_query_handler(filters.Text('next'), state=SubcategoryState.CONCERT)
async def select_theatre_subcategories(callback: CallbackQuery, state: FSMContext):
    await SubcategoryState.THEATRE.set()
    user_data = await state.get_data()
    if 'THEATRE' in user_data['CATEGORIES']:
        if 'USER_KEYBOARD_THEATRE_SUBCATEGORIES' in user_data:
            keyboard = user_data['USER_KEYBOARD_THEATRE_SUBCATEGORIES']
        else:
            keyboard = keyboard_setting_subcategories_theatre()
            await state.update_data(USER_KEYBOARD_THEATRE_SUBCATEGORIES=keyboard)
        await callback.message.answer("Ты выбрал категорию \"Театр\". Какие постановки ты любишь?",
                                      reply_markup=keyboard)
    else:
        await select_show_subcategories(callback, state)
        print('Театр не выбрано')
    await callback.answer()

@dp.callback_query_handler(filters.Text(endswith='_NO'), state=SubcategoryState.THEATRE)
async def add_theatre_subcategory(callback: CallbackQuery, state: FSMContext) -> None:
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
    await callback.message.edit_text("Ты выбрал категорию \"Театр\". Какие постановки ты любишь?",
                                     reply_markup=keyboard)
    await callback.answer()

@dp.callback_query_handler(filters.Text(endswith='_YES'), state=SubcategoryState.THEATRE)
async def delete_subcategory(callback: CallbackQuery, state: FSMContext) -> None:
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
    await callback.message.edit_text("Ты выбрал категорию \"Театр\". Какие постановки ты любишь?",
                                     reply_markup=keyboard)
    await callback.answer()

#-----------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(filters.Text('next'), state=SubcategoryState.THEATRE)
async def select_show_subcategories(callback: CallbackQuery, state: FSMContext):
    await SubcategoryState.SHOW.set()
    user_data = await state.get_data()
    if 'SHOW' in user_data['CATEGORIES']:
        if 'USER_KEYBOARD_SHOW_SUBCATEGORIES' in user_data:
            keyboard = user_data['USER_KEYBOARD_SHOW_SUBCATEGORIES']
        else:
            keyboard = keyboard_setting_subcategories_show()
            await state.update_data(USER_KEYBOARD_SHOW_SUBCATEGORIES=keyboard)
        await callback.message.answer("Ты выбрал категорию \"Шоу\". Что тебя интересует?", reply_markup=keyboard)
    else:
        print('Шоу не выбрано')
        await select_followweek(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text(endswith='_NO'), state=SubcategoryState.SHOW)
async def add_subcategory(callback: CallbackQuery, state: FSMContext) -> None:
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
    await callback.answer()

@dp.callback_query_handler(filters.Text(endswith='_YES'), state=SubcategoryState.SHOW)
async def delete_subcategory(callback: CallbackQuery, state: FSMContext) -> None:
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
    await callback.answer()

########################################################################################################################
@dp.callback_query_handler(filters.Text('next'), state=SubcategoryState.SHOW)
async def select_followweek(callback: CallbackQuery, state: FSMContext):
    await UserState.FOLOWWEEK.set()
    await callback.message.answer("Последний вопрос: "
                                  "нужна ли тебе рассылка мероприятий по понедельникам?",
                                  reply_markup=keyboard_setting_followweek())
    await callback.answer()


@dp.callback_query_handler(filters.Text('followweek_NO'), state=UserState.FOLOWWEEK)
async def followweek_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Настройка окончена!')
    await state.update_data(FOLLOWWEEK=False)
    await UserState.WAIT.set()
    await callback.answer()


@dp.callback_query_handler(filters.Text('followweek_YES'), state=UserState.FOLOWWEEK)
async def followweek_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Настройка окончена!')
    await state.update_data(FOLLOWWEEK=True)
    await UserState.WAIT.set()
    await callback.answer()

########################################################################################################################
@dp.message_handler(commands=['info'], state=UserState.WAIT)
async def info(message: types.Message):
    await message.answer('EventsNN - это бот для поиска мероприятий в Нижнем Новгороде. '
                         'С помощью него вы с легкостью найдете мероприятие на свой вкус.\n\n'
                         'Доступные команды:\n'
                         '/events - просмотр мероприятий по категориям\n'
                         '/settings - настроить подписку на категории\n'
                         '/info - информация о боте и все команды')

########################################################################################################################
@dp.message_handler(commands=['events'], state=UserState.WAIT)
async def events(message: types.Message):
    await EventsState.CATEGORY.set()
    await message.answer('Какая категория тебя интересует?', reply_markup=keyboard_event_categories())
# -----------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(filters.Text('cinema'), state=EventsState.CATEGORY)
async def cinema_category(callback: CallbackQuery, state: FSMContext):
    await EventsState.SUBCATEGORY.set()
    await callback.message.answer('Какая категория тебя интересует?',
                                  reply_markup=keyboard_event_cinema_subcategories())
    await EventsState.PRINT_EVENT.set()
    await callback.answer()

@dp.callback_query_handler(filters.Text('cinema_action'), state=EventsState.PRINT_EVENT)
async def cinema_action(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='CINEMA' AND subcategory='CINEMA_ACTION'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('cinema_drama'), state=EventsState.PRINT_EVENT)
async def cinema_drama(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='CINEMA' AND subcategory='CINEMA_DRAMA'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('cinema_comedy'), state=EventsState.PRINT_EVENT)
async def cinema_comedy(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='CINEMA' AND subcategory='CINEMA_COMEDY'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('cinema_romance'), state=EventsState.PRINT_EVENT)
async def cinema_romance(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='CINEMA' AND subcategory='CINEMA_ROMANCE'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('cinema_adventure'), state=EventsState.PRINT_EVENT)
async def cinema_adventure(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='CINEMA' AND subcategory='CINEMA_ADVENTURE'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('cinema_thriller'), state=EventsState.PRINT_EVENT)
async def cinema_thriller(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='CINEMA' AND subcategory='CINEMA_THRILLER'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('cinema_horror'), state=EventsState.PRINT_EVENT)
async def cinema_horror(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='CINEMA' AND subcategory='CINEMA_HORROR'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('cinema_fiction'), state=EventsState.PRINT_EVENT)
async def cinema_fiction(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='CINEMA' AND subcategory='CINEMA_FICTION'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('cinema_cartoon'), state=EventsState.PRINT_EVENT)
async def cinema_cartoon(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='CINEMA' AND subcategory='CINEMA_CARTOON'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()
# -----------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(filters.Text('concert'), state=EventsState.CATEGORY)
async def concert_category(callback: CallbackQuery, state: FSMContext):
    await EventsState.SUBCATEGORY.set()
    await callback.message.answer('Какая категория тебя интересует?',
                                  reply_markup=keyboard_event_concert_subcategories())
    await EventsState.PRINT_EVENT.set()
    await callback.answer()
    await callback.answer()

@dp.callback_query_handler(filters.Text('concert_pop'), state=EventsState.PRINT_EVENT)
async def concert_pop(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='CONCERT' AND subcategory='CONCERT_POP'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('concert_hiphop_rap'), state=EventsState.PRINT_EVENT)
async def concert_hiphop_rap(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='CONCERT' AND subcategory='CONCERT_HIPHOP_RAP'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('concert_rock'), state=EventsState.PRINT_EVENT)
async def concert_rock(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='CONCERT' AND subcategory='CONCERT_ROCK'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('concert_methal'), state=EventsState.PRINT_EVENT)
async def concert_methal(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='CONCERT' AND subcategory='CONCERT_METHAL'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('concert_classicalmusic'), state=EventsState.PRINT_EVENT)
async def concert_classicalmusic(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='CONCERT' AND subcategory='CONCERT_CLASSICAL_MUSIC'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()
# -----------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(filters.Text('theatre'), state=EventsState.CATEGORY)
async def theatre_category(callback: CallbackQuery, state: FSMContext):
    await EventsState.SUBCATEGORY.set()
    await callback.message.answer('Какая категория тебя интересует?',
                                  reply_markup=keyboard_event_theatre_subcategories())
    await EventsState.PRINT_EVENT.set()
    await callback.answer()

@dp.callback_query_handler(filters.Text('theatre_comedy'), state=EventsState.PRINT_EVENT)
async def theatre_comedy(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='THEATRE' AND subcategory='THEATRE_COMEDY'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('theatre_drama'), state=EventsState.PRINT_EVENT)
async def theatre_drama(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='THEATRE' AND subcategory='THEATRE_DRAMA'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('theatre_monoperformance'), state=EventsState.PRINT_EVENT)
async def theatre_monoperformance(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='THEATRE' AND subcategory='THEATRE_MONOPERFORMANCE'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('theatre_musical'), state=EventsState.PRINT_EVENT)
async def theatre_musical(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='THEATRE' AND subcategory='THEATRE_MUSICAL'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()
# -----------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(filters.Text('show'), state=EventsState.CATEGORY)
async def show_category(callback: CallbackQuery, state: FSMContext):
    await EventsState.SUBCATEGORY.set()
    await callback.message.answer('Какая категория тебя интересует?', reply_markup=keyboard_event_show_subcategories())
    await EventsState.PRINT_EVENT.set()
    await callback.answer()

@dp.callback_query_handler(filters.Text('show_standup'), state=EventsState.PRINT_EVENT)
async def show_standup(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='SHOW' AND subcategory='SHOW_STANDUP'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('show_kids'), state=EventsState.PRINT_EVENT)
async def show_kids(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='SHOW' AND subcategory='SHOW_KIDS'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

@dp.callback_query_handler(filters.Text('show_nonchildren'), state=EventsState.PRINT_EVENT)
async def show_nonchildren(callback: CallbackQuery, state: FSMContext):
    await state.update_data(REQUIRED_EVENTS=duckdb.sql(
        "SELECT * FROM 'eventsDB.parquet' WHERE category='SHOW' AND subcategory='SHOW_NON_CHILDREN'").fetchall())
    await start_print_events(callback, state)
    await callback.answer()

# -----------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(filters.Text('all'), state=EventsState.CATEGORY)
async def all_category(callback: CallbackQuery, state: FSMContext):
    await EventsState.PRINT_EVENT.set()
    EVENTS = duckdb.sql("SELECT * FROM 'eventsDB.parquet'").fetchall()
    random.shuffle(EVENTS)
    await state.update_data(REQUIRED_EVENTS=EVENTS)
    await state.update_data(NUMBER_OF_EVENT=0)
    await print_next_event(callback, state)
    await callback.answer()

# -----------------------------------------------------------------------------------------------------------------------
@dp.message_handler(state=EventsState.PRINT_EVENT)
async def start_print_events(callback: CallbackQuery, state: FSMContext):
    await state.update_data(NUMBER_OF_EVENT=0)
    await callback.answer()
    await print_next_event(callback, state)

@dp.callback_query_handler(filters.Text('next'), state=EventsState.PRINT_EVENT)
async def print_next_event(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if user_data['NUMBER_OF_EVENT'] == len(user_data['REQUIRED_EVENTS']):
        await callback.message.answer('Это все мероприятия в данной категории!')
        await UserState.WAIT.set()
    else:
        photo, caption = make_card(user_data['NUMBER_OF_EVENT'], user_data['REQUIRED_EVENTS'])
        await callback.message.bot.send_photo(chat_id=callback.message.chat.id, photo=photo, caption=caption,
                                              reply_markup=keyboard_commands())
        await state.update_data(NUMBER_OF_EVENT=user_data['NUMBER_OF_EVENT'] + 1)
    await callback.answer()

@dp.callback_query_handler(filters.Text('exit'), state=[state for state in
                                                        [EventsState.PRINT_EVENT, EventsState.CATEGORY,
                                                         EventsState.SUBCATEGORY]])
async def exit_from_list(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Вы вышли!')
    await UserState.WAIT.set()
    await callback.answer()

########################################################################################################################
@dp.message_handler(commands=['settings'], state=UserState.WAIT)
async def settings(message: types.Message, state: FSMContext):
    await UserState.CATEGORIES.set()
    await select_categories(message, state)


########################################################################################################################
executor.start_polling(dp)
