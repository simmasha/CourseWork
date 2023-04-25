#import telebot
from aiogram import Bot, Dispatcher, executor, types

bot = Bot('6025564381:AAE0nNtkoOrNBNstPQFexvEVdyh_U9kNlsA')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message): #(message: types.message)
    await bot.send_sticker(message.from_user.id, sticker='CAACAgQAAxkBAAEIuJFkR6hI7xeNZE6F0DZix_p7geY8IAACawADzjkIDVlm6mN2kkvQLwQ')
    await message.answer(f'Привет, {message.from_user.first_name}!🙌\nДля начала предлагаю настроить бота для твоего удобства')
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Кино', callback_data='cinema')
    btn2 = types.InlineKeyboardButton('Театр', callback_data='theatre')
    btn3 = types.InlineKeyboardButton('Концерты', callback_data='concert')
    btn4 = types.InlineKeyboardButton('Выставки', callback_data='exhibition')
    btn5 = types.InlineKeyboardButton('Дальше➡️', callback_data='next')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)
    await message.answer('Выбери категории, которые тебя интересуют', reply_markup=markup)

@dp.callback_query_handler()
async def callback_message(callback):
    if callback.data == 'next':
        await callback.message.delete()
        markup = types.InlineKeyboardMarkup()
        btn6 = types.InlineKeyboardButton('Подписаться на еженедельную рассылку', callback_data='followweek')
        btn7 = types.InlineKeyboardButton('Уведомлять о новых событиях', callback_data='follownew')
        btn8 = types.InlineKeyboardButton('Завершить настройку🏁', callback_data='finish')
        markup.add(btn6)
        markup.add(btn7)
        markup.add(btn8)
        await callback.message.answer('Какие уведомления ты хочешь получать?\n'
                                      'У нас есть рассылка мероприятий на неделю по понедельникам, '
                                      'а также уведомления о новых мероприятиях в выбранных тобой категориях.'
                                      '\nМожно выбрать обе рассылки', reply_markup=markup)
    elif callback.data == 'finish':
        #await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await callback.message.delete()
        await callback.message.answer('Настройка окончена!')


@dp.message_handler(commands=['info'])
async def info(message):
    await message.answer('EventsNN - это бот для поиска мероприятий в Нижнем Новгороде. '
                                     'С помощью него вы с легкостью найдете мероприятие на свой вкус.\n')

@dp.message_handler(commands=['events'])
async def events(message):
    pass

executor.start_polling(dp)
