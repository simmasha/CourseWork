from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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

def make_card(index: int, array: list):
    photo = array[index][6]
    title = array[index][3]
    date = array[index][5]
    place = array[index][4]
    link = array[index][7]
    caption = f'{title}\nКогда: {date}\nГде:{place}\nПодробная информация и билеты:{link}'
    return photo, caption