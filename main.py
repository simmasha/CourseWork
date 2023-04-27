from aiogram import Bot, Dispatcher, executor, types
import requests
from bs4 import BeautifulSoup

URL = 'https://afisha.yandex.ru/nizhny-novgorod/cinema?source=menu&preset=today'
r = requests.get(URL)
print(r)
soup = BeautifulSoup(r.text, 'html.parser')
#events = soup.find_all('div', class_='Root-fq4hbj-4 iFrhLC')
events = soup.find_all('h2', class_='Title-fq4hbj-3 hponhw')
events_t = [c.text for c in events]
print(events_t)

print("\n")

bot = Bot('6025564381:AAE0nNtkoOrNBNstPQFexvEVdyh_U9kNlsA')
dp = Dispatcher(bot)

markup1, markup2 = types.InlineKeyboardMarkup(), types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Кино', callback_data='cinemaNo')
btn2 = types.InlineKeyboardButton('Театр', callback_data='theatreNo')
btn3 = types.InlineKeyboardButton('Концерты', callback_data='concertNo')
btn4 = types.InlineKeyboardButton('Выставки', callback_data='exhibitionNo')
btn5 = types.InlineKeyboardButton('Дальше➡️', callback_data='next')

btn6 = types.InlineKeyboardButton('Подписаться на еженедельную рассылку', callback_data='followweekNo')
btn7 = types.InlineKeyboardButton('Уведомлять о новых событиях', callback_data='follownewNo')
btn8 = types.InlineKeyboardButton('Завершить настройку🏁', callback_data='finish')

########################################################################################################################

#обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message): #(message: types.message)
    await bot.send_sticker(message.from_user.id, sticker='CAACAgQAAxkBAAEIuJFkR6hI7xeNZE6F0DZix_p7geY8IAACawADzjkIDVlm6mN2kkvQLwQ')
    await message.answer(f'Привет, {message.from_user.first_name}!🙌\nДля начала предлагаю настроить бота для твоего удобства')
    #markup = types.InlineKeyboardMarkup()
    markup1.row(btn1, btn2)
    markup1.row(btn3, btn4)
    markup1.row(btn5)
    await message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)

########################################################################################################################

#обработчик нажатий на кнопки
@dp.callback_query_handler()
async def callback_message(callback):
    #кнопка 'дальше'
    if callback.data == 'next':
        await callback.message.delete()
        markup2.add(btn6)
        markup2.add(btn7)
        markup2.add(btn8)
        await callback.message.answer('Какие уведомления ты хочешь получать?\n'
                                      'У нас есть рассылка мероприятий на неделю по понедельникам, '
                                      'а также уведомления о новых мероприятиях в выбранных тобой категориях.'
                                      '\nМожно выбрать обе рассылки', reply_markup=markup2)

    #кнопка 'завершить настройку'
    elif callback.data == 'finish':
        #await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await callback.message.delete()
        await callback.message.answer('Настройка окончена!')

    #кино выбрано/не выбрано
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

    #театр выбран/не выбран
    elif callback.data == 'theatreNo':
        btn2.text = '✅ Театр'
        btn2.callback_data = 'theatreYes'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)
    elif callback.data == 'theatreYes':
        btn2.text = 'Театр'
        btn2.callback_data = 'theatreNo'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)

    # концерты выбраны/не выбраны
    elif callback.data == 'concertNo':
        btn3.text = '✅ Концерты'
        btn3.callback_data = 'concertYes'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)
    elif callback.data == 'concertYes':
        btn3.text = 'Концерты'
        btn3.callback_data = 'concertNo'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)

    # выставки выбраны/не выбраны
    elif callback.data == 'exhibitionNo':
        btn4.text = '✅ Выставки'
        btn4.callback_data = 'exhibitionYes'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)
    elif callback.data == 'exhibitionYes':
        btn4.text = 'Выставки'
        btn4.callback_data = 'exhibitionNo'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup1)

    # еженедельная рассылка нужна/не нужна
    elif callback.data == 'followweekNo':
        btn6.text = '✅ Подписаться на еженедельную рассылку'
        btn6.callback_data = 'followweekYes'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup2)
    elif callback.data == 'followweekYes':
        btn6.text = 'Подписаться на еженедельную рассылку'
        btn6.callback_data = 'followweekNo'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup2)

    # еженедельная рассылка нужна/не нужна
    elif callback.data == 'follownewNo':
        btn7.text = '✅ Уведомлять о новых событиях'
        btn7.callback_data = 'follownewYes'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup2)
    elif callback.data == 'follownewYes':
        btn7.text = 'Уведомлять о новых событиях'
        btn7.callback_data = 'follownewNo'
        await callback.message.delete()
        await callback.message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup2)


########################################################################################################################

@dp.message_handler(commands=['info'])
async def info(message):
    await message.answer('EventsNN - это бот для поиска мероприятий в Нижнем Новгороде. '
                                     'С помощью него вы с легкостью найдете мероприятие на свой вкус.\n')

########################################################################################################################

@dp.message_handler(commands=['events'])
async def events(message):
    #await message.answer('У нас пока нет мероприятий😢')
    await message.answer('Сегодня в кино:')
    await message.answer(events_t)

########################################################################################################################

executor.start_polling(dp)
