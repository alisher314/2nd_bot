from telebot import types

# Кнопка отправки номера
def num_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Отправить номер�', request_contact=True)
    kb.add(but1)
    return kb

# Кнопка отправки геолокации
def location_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Отправить геолокацию📍', request_location=True)
    kb.add(but1)
    return kb

# Основное меню
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1) # Устанавливаем ширину ряда для кнопок
    # Добавляем новую кнопку "Мой профиль"
    kb.add(types.KeyboardButton('Мой профиль'))
    # Кнопка "Остановить бота" удалена
    return kb