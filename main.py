import telebot
from telebot import types

bot = telebot.TeleBot('6025564381:AAE0nNtkoOrNBNstPQFexvEVdyh_U9kNlsA')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nДля начала предлагаю настроить бота для твоего удобства')
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Кино', callback_data='cinema')
    btn2 = types.InlineKeyboardButton('Театр', callback_data='theatre')
    btn3 = types.InlineKeyboardButton('Концерты', callback_data='concert')
    btn4 = types.InlineKeyboardButton('Выставки', callback_data='exhibition')
    btn5 = types.InlineKeyboardButton('Дальше', callback_data='next')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)
    bot.send_message(message.chat.id, 'Выбери категории, которые тебя интересуют', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback:True)
def callback_message(callback):
    if callback.data == 'next':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Подписаться на еженедельную рассылку', callback_data='followweek')
        btn2 = types.InlineKeyboardButton('Уведомлять о новых событиях', callback_data='follownew')
        btn3 = types.InlineKeyboardButton('Завершить настройку', callback_data='finish')
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        bot.send_message(callback.message.chat.id, 'Какие уведомления ты хочешь получать?\n'
                                                   'У нас есть рассылка мероприятий на неделю по понедельникам, '
                                                   'а также уведомления о новых мероприятиях в выбранных тобой категориях.'
                                                   '\nМожно выбрать обе рассылки', reply_markup=markup)
    elif callback.data == 'finish': bot.send_message(callback.message.chat.id, 'Настройка окончена!')


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, 'EventsNN - это бот для поиска мероприятий в Нижнем Новгороде. '
                                     'С помощью него вы с легкостью найдете мероприятие на свой вкус.\n')


bot.polling(none_stop=True)

