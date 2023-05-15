from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def keyboard_setting_categories() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Кино', callback_data='cinema_NO'),
        InlineKeyboardButton('Концерты', callback_data='concert_NO'),
        InlineKeyboardButton('Театр', callback_data='theatre_NO'),
        InlineKeyboardButton('Шоу', callback_data='show_NO'),
        InlineKeyboardButton('Дальше➡️', callback_data='next')
    ]
    button_cancel = InlineKeyboardButton('Не настраивать категории❌', callback_data='cancel')
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    keyboard.add(button_cancel)
    return keyboard

def keyboard_setting_subcategories_cinema() -> InlineKeyboardMarkup:
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

def keyboard_setting_subcategories_concert() -> InlineKeyboardMarkup:
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

def keyboard_setting_subcategories_theatre() -> InlineKeyboardMarkup:
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

def keyboard_setting_subcategories_show() -> InlineKeyboardMarkup:
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

def keyboard_setting_followweek() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Да', callback_data='followweek_YES'),
        InlineKeyboardButton('Нет', callback_data='followweek_NO'),
    ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

def keyboard_event_categories() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Кино', callback_data='cinema'),
        InlineKeyboardButton('Концерты', callback_data='concert'),
        InlineKeyboardButton('Театр', callback_data='theatre'),
        InlineKeyboardButton('Шоу', callback_data='show'),
        InlineKeyboardButton('Все', callback_data='all')
    ]
    button_exit = InlineKeyboardButton('Выход❌', callback_data='exit')
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    keyboard.add(button_exit)
    return keyboard


def keyboard_event_cinema_subcategories() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Боевик', callback_data='cinema_action'),
        InlineKeyboardButton('Драма', callback_data='cinema_drama'),
        InlineKeyboardButton('Комедия', callback_data='cinema_comedy'),
        InlineKeyboardButton('Мелодрама', callback_data='cinema_romance'),
        InlineKeyboardButton('Приключения', callback_data='cinema_adventure'),
        InlineKeyboardButton('Триллер', callback_data='cinema_thriller'),
        InlineKeyboardButton('Ужасы', callback_data='cinema_horror'),
        InlineKeyboardButton('Фантастика', callback_data='cinema_fiction'),
        InlineKeyboardButton('Мультфильмы', callback_data='cinema_cartoon'),
    ]
    button_exit = InlineKeyboardButton('Выход❌', callback_data='exit')
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    keyboard.add(button_exit)
    return keyboard


def keyboard_event_concert_subcategories() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Поп', callback_data='concert_pop'),
        InlineKeyboardButton('Хип-хоп и рэп', callback_data='concert_hiphop_rap'),
        InlineKeyboardButton('Рок', callback_data='concert_rock'),
        InlineKeyboardButton('Металл', callback_data='concert_methal'),
        InlineKeyboardButton('Классическая музыка', callback_data='concert_classicalmusic')
    ]
    button_exit = InlineKeyboardButton('Выход❌', callback_data='exit')
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    keyboard.add(button_exit)
    return keyboard


def keyboard_event_theatre_subcategories() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Комедия', callback_data='theatre_comedy'),
        InlineKeyboardButton('Драма', callback_data='theatre_drama'),
        InlineKeyboardButton('Моноспектакль', callback_data='theatre_monoperformance'),
        InlineKeyboardButton('Мьюзикл', callback_data='theatre_musical'),
    ]
    button_exit = InlineKeyboardButton('Выход❌', callback_data='exit')
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    keyboard.add(button_exit)
    return keyboard


def keyboard_event_show_subcategories() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Стендап', callback_data='show_standup'),
        InlineKeyboardButton('Детям', callback_data='show_kids'),
        InlineKeyboardButton('Без детей', callback_data='show_nonchildren'),
    ]
    button_exit = InlineKeyboardButton('Выход❌', callback_data='exit')
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    keyboard.add(button_exit)
    return keyboard


def keyboard_commands() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton('Дальше➡️', callback_data='next'),
        InlineKeyboardButton('Напомнить🔔', callback_data='remind'),
        InlineKeyboardButton('Выход❌', callback_data='exit')
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard