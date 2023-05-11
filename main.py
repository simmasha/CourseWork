from parsing import *
import duckdb
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message

#проблемы:
#ривести дату в нормальный вид, иначе не сможем настроить напоминание о событии

bot = Bot('6025564381:AAE0nNtkoOrNBNstPQFexvEVdyh_U9kNlsA')
dp = Dispatcher(bot)

markup1, markup2, markup_next = types.InlineKeyboardMarkup(), types.InlineKeyboardMarkup(), types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Кино', callback_data='cinemaNo')
btn2 = types.InlineKeyboardButton('Концерты', callback_data='concertNo')
btn3 = types.InlineKeyboardButton('Театр', callback_data='theatreNo')
btn4 = types.InlineKeyboardButton('Пушкинская карта', callback_data='pushkincardNo')
# btn5 = types.InlineKeyboardButton('Квесты', callback_data='questNo')
btn6 = types.InlineKeyboardButton('Шоу', callback_data='showNo')
btn7 = types.InlineKeyboardButton('Стендап', callback_data='standupNo')
btn8 = types.InlineKeyboardButton('Экскурсии', callback_data='excursionNo')
btn9 = types.InlineKeyboardButton('Мюзиклы', callback_data='musicalNo')
btn10 = types.InlineKeyboardButton('Мастер-классы', callback_data='maserclassNo')
# btn11 = types.InlineKeyboardButton('Дальше➡️', callback_data='next')
# btn12 = types.InlineKeyboardButton('Подписаться на еженедельную рассылку', callback_data='followweekNo')
# btn13 = types.InlineKeyboardButton('Уведомлять о новых событиях', callback_data='follownewNo')
btn11 = types.InlineKeyboardButton('Завершить настройку🏁', callback_data='finish')

btn_cinema = types.InlineKeyboardButton('Кино', callback_data='CINEMA')
btn_concert = types.InlineKeyboardButton('Концерты', callback_data='CONCERT')
btn_theatre = types.InlineKeyboardButton('Театр', callback_data='THEATRE')
btn_pcard = types.InlineKeyboardButton('Пушкинская карта', callback_data='PUSHKIN_CARD')
# btn_quest = types.InlineKeyboardButton('Квесты', callback_data='QUEST')
btn_show = types.InlineKeyboardButton('Шоу', callback_data='SHOW')
btn_standup = types.InlineKeyboardButton('Стендап', callback_data='STANDUP')
btn_excursion = types.InlineKeyboardButton('Экскурсии', callback_data='EXCURSION')
btn_musical = types.InlineKeyboardButton('Мюзиклы', callback_data='MUSICAL')
btn_mclass = types.InlineKeyboardButton('Мастер-классы', callback_data='MASTERCLASS')
btn_next = types.InlineKeyboardButton('Дальше', callback_data='NEXT_EVENT')

markup1.row(btn1, btn2)
markup1.row(btn3, btn4)
# markup1.row(btn5, btn6)
markup1.row(btn7, btn8)
markup1.row(btn9, btn10)
markup1.row(btn6)
markup1.row(btn11)

markup_next.row(btn_next)

markup = types.InlineKeyboardMarkup()
markup.row(btn_cinema, btn_concert)
markup.row(btn_theatre, btn_pcard)
# markup.row(btn_quest, btn_show)
markup.row(btn_show)
markup.row(btn_standup, btn_excursion)
markup.row(btn_musical, btn_mclass)

#     markup2.add(btn6)
#     markup2.add(btn7)
#     markup2.add(btn8)

EVENTS = None
position = None
length = None

Parsing()

########################################################################################################################

# обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: Message):
    await bot.send_sticker(message.from_user.id,
                           sticker='CAACAgQAAxkBAAEIuJFkR6hI7xeNZE6F0DZix_p7geY8IAACawADzjkIDVlm6mN2kkvQLwQ')
    await message.answer( f'Привет, {message.from_user.first_name}!🙌\nДля начала предлагаю настроить бота для твоего удобства')
    await message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)


########################################################################################################################

# обработчик нажатий на кнопки
@dp.callback_query_handler()
async def callback_message(callback: types.CallbackQuery):
    global EVENTS, position, length
    # кнопка 'дальше'
    # if callback.data == 'next':
    #     await callback.message.delete()

    #     await callback.message.answer('Какие уведомления ты хочешь получать?\n'
    #                                   'У нас есть рассылка мероприятий на неделю по понедельникам, '
    #                                   'а также уведомления о новых мероприятиях в выбранных тобой категориях.'
    #                                   '\nМожно выбрать обе рассылки', reply_markup=markup2)

    # кнопка 'завершить настройку'
    if callback.data == 'finish':
        # await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await callback.message.delete()
        await callback.message.answer('Настройка окончена!')

    #elif callback.data in ['cinemaNo', 'concertNo', 'theatreNo', 'pushkincardNo', 'questNo', 'showNo', 'standupNo', 'excursionNo', 'musicalNo', 'maserclassNo']:

    # кино выбрано/не выбрано
    elif callback.data == 'cinemaNo':
        btn1.text = '✅ Кино'
        btn1.callback_data = 'cinemaYes'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)
    elif callback.data == 'cinemaYes':
        btn1.text = 'Кино'
        btn1.callback_data = 'cinemaNo'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)

    # концерты выбраны/не выбраны
    elif callback.data == 'concertNo':
        btn2.text = '✅ Концерты'
        btn2.callback_data = 'concertYes'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)
    elif callback.data == 'concertYes':
        btn2.text = 'Концерты'
        btn2.callback_data = 'concertNo'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)

    # театр выбран/не выбран
    elif callback.data == 'theatreNo':
        btn3.text = '✅ Театр'
        btn3.callback_data = 'theatreYes'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)
        # концерты выбраны/не выбраны
    elif callback.data == 'theatreYes':
        btn3.text = 'Театр'
        btn3.callback_data = 'theatreNo'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)

    # Пушкинская карта выбрано/не выбрано
    elif callback.data == 'pushkincardNo':
        btn4.text = '✅ Пушкинская карта'
        btn4.callback_data = 'pushkincardYes'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)
    elif callback.data == 'pushkincardYes':
        btn4.text = 'Пушкинская карта'
        btn4.callback_data = 'pushkincardNo'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)

    # # Квесты выбраны/не выбраны
    # elif callback.data == 'questNo':
    #     btn5.text = '✅ Квесты'
    #     btn5.callback_data = 'questYes'
    #     await callback.message.delete()
    #     await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)
    # elif callback.data == 'questYes':
    #     btn5.text = 'Квесты'
    #     btn5.callback_data = 'questNo'
    #     await callback.message.delete()
    #     await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)

    # Шоу выбраны/не выбраны
    elif callback.data == 'showNo':
        btn6.text = '✅ Шоу'
        btn6.callback_data = 'showYes'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)
    elif callback.data == 'showYes':
        btn6.text = 'Шоу'
        btn6.callback_data = 'showNo'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)

    # Стендап выбран/не выбран
    elif callback.data == 'standupNo':
        btn7.text = '✅ Стендап'
        btn7.callback_data = 'standupYes'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)
    elif callback.data == 'standupYes':
        btn7.text = 'Стендап'
        btn7.callback_data = 'standupNo'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)

    # экскурсии выбраны/не выбраны
    elif callback.data == 'excursionNo':
        btn8.text = '✅ Экскурсии'
        btn8.callback_data = 'excursionYes'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)
    elif callback.data == 'excursionYes':
        btn8.text = 'Экскурсии'
        btn8.callback_data = 'excursionNo'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)

    # Мюзиклы выбраны/не выбраны
    elif callback.data == 'musicalNo':
        btn9.text = '✅ Мюзиклы'
        btn9.callback_data = 'musicalYes'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)
    elif callback.data == 'musicalYes':
        btn9.text = 'Мюзиклы'
        btn9.callback_data = 'musicalNo'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)

    # Мастер-классы выбраны/не выбраны
    elif callback.data == 'maserclassNo':
        btn9.text = '✅ Мастер-классы'
        btn9.callback_data = 'maserclassYes'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)
    elif callback.data == 'maserclassYes':
        btn9.text = 'Мастер-классы'
        btn9.callback_data = 'maserclassNo'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)

    # еженедельная рассылка нужна/не нужна
    # elif callback.data == 'followweekNo':
    #     btn6.text = '✅ Подписаться на еженедельную рассылку'
    #     btn6.callback_data = 'followweekYes'
    #     await callback.message.delete()
    #     await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup2)
    # elif callback.data == 'followweekYes':
    #     btn6.text = 'Подписаться на еженедельную рассылку'
    #     btn6.callback_data = 'followweekNo'
    #     await callback.message.delete()
    #     await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup2)
    #
    # # еженедельная рассылка нужна/не нужна
    # elif callback.data == 'follownewNo':
    #     btn7.text = '✅ Уведомлять о новых событиях'
    #     btn7.callback_data = 'follownewYes'
    #     await callback.message.delete()
    #     await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup2)
    # elif callback.data == 'follownewYes':
    #     btn7.text = 'Уведомлять о новых событиях'
    #     btn7.callback_data = 'follownewNo'
    #     await callback.message.delete()
    #     await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup2)

    elif callback.data in ['CINEMA', 'CONCERT', 'THEATRE', 'PUSHKIN_CARD', 'QUEST', 'SHOW', 'STANDUP', 'EXCURSION', 'MUSICAL', 'MASTERCLASS']:
        if callback.data == 'CINEMA': EVENTS = duckdb.sql("SELECT * FROM 'events_file.parquet' WHERE category='CINEMA'").fetchall()
        elif callback.data == 'CONCERT': EVENTS = duckdb.sql("SELECT * FROM 'events_file.parquet' WHERE category='CONCERT'").fetchall()
        elif callback.data == 'THEATRE': EVENTS = duckdb.sql("SELECT * FROM 'events_file.parquet' WHERE category='THEATRE'").fetchall()
        elif callback.data == 'PUSHKIN_CARD': EVENTS = duckdb.sql("SELECT * FROM 'events_file.parquet' WHERE category='PUSHKIN_CARD'").fetchall()
        elif callback.data == 'QUEST': EVENTS = duckdb.sql("SELECT * FROM 'events_file.parquet' WHERE category='QUEST'").fetchall()
        elif callback.data == 'SHOW': EVENTS = duckdb.sql("SELECT * FROM 'events_file.parquet' WHERE category='SHOW'").fetchall()
        elif callback.data == 'STANDUP': EVENTS = duckdb.sql("SELECT * FROM 'events_file.parquet' WHERE category='STANDUP'").fetchall()
        elif callback.data == 'EXCURSION': EVENTS = duckdb.sql("SELECT * FROM 'events_file.parquet' WHERE category='EXCURSION'").fetchall()
        elif callback.data == 'MUSICAL': EVENTS = duckdb.sql("SELECT * FROM 'events_file.parquet' WHERE category='MUSICAL'").fetchall()
        elif callback.data == 'MASTERCLASS': EVENTS = duckdb.sql("SELECT * FROM 'events_file.parquet' WHERE category='MASTERCLASS'").fetchall()

        #не работает, так как колбэк переносится в двойных кавычках, а sql такого не понимать
        #EVENTS = duckdb.sql(f"SELECT * FROM 'events_file.parquet' WHERE category={callback.data}").fetchall()


        length = len(EVENTS)
        position = 0

        #добавить проверку есть ли место или время
        await callback.message.bot.send_photo(chat_id=callback.message.chat.id, photo=EVENTS[position][5],
                                              caption=f'{EVENTS[position][2]}\n'
                                                      f'Когда: {EVENTS[position][4]}\n'
                                                      f'Где: {EVENTS[position][3]}\n'
                                                      f'Ссылка на покупку: {EVENTS[position][6]}',
                                              reply_markup=markup_next)
        position += 1
        await bot.answer_callback_query(callback.id)

    elif callback.data == 'NEXT_EVENT':
        if position == length:
            await callback.message.answer('Конец(')
            EVENTS = None
            position = None
            length = None
        else:
            await callback.message.bot.send_photo(chat_id=callback.message.chat.id, photo=EVENTS[position][5],
                                                  caption=f'{EVENTS[position][2]}\n'
                                                          f'Когда: {EVENTS[position][4]}\n'
                                                          f'Где: {EVENTS[position][3]}\n'
                                                          f'Ссылка на покупку: {EVENTS[position][6]}',
                                                  reply_markup=markup_next)

            position += 1
    else:
        await callback.answer()



########################################################################################################################

@dp.message_handler(commands=['info'])
async def info(message):
    await message.answer('EventsNN - это бот для поиска мероприятий в Нижнем Новгороде. '
                         'С помощью него вы с легкостью найдете мероприятие на свой вкус.\n')


########################################################################################################################

@dp.message_handler(commands=['events'])
async def events(message):

    await message.answer('Какая категория тебя интересует?', reply_markup=markup)


########################################################################################################################

executor.start_polling(dp)
