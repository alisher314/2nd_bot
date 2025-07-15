from telebot import types
# Импортируем модуль 'types' из библиотеки 'telebot'.

# Мы не можем импортировать MESSAGES напрямую здесь, так как это приведет к циклической зависимости
# (bot.py импортирует buttons.py, а buttons.py будет импортировать bot.py).
# Вместо этого, функции будут принимать словарь messages и код языка.

# Кнопка отправки номера
def num_button(messages, lang_code):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Используем текст из словаря messages для текущего языка
    but1 = types.KeyboardButton(messages[lang_code]['send_number_button'], request_contact=True)
    kb.add(but1)
    return kb

# Кнопка отправки геолокации
def location_button(messages, lang_code):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Используем текст из словаря messages для текущего языка
    but1 = types.KeyboardButton(messages[lang_code]['send_location_button'], request_location=True)
    kb.add(but1)
    return kb

# Основное меню
def main_menu(messages, lang_code):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    # Используем тексты из словаря messages для текущего языка
    kb.add(types.KeyboardButton(messages[lang_code]['my_profile_button']))
    kb.add(types.KeyboardButton(messages[lang_code]['settings_button']))
    return kb

# Меню настроек
def settings_menu(messages, lang_code):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    # Используем тексты из словаря messages для текущего языка
    kb.add(types.KeyboardButton(messages[lang_code]['change_lang_button']))
    kb.add(types.KeyboardButton(messages[lang_code]['back_to_main_button']))
    return kb

# Меню выбора языка (InlineKeyboardMarkup) - тексты кнопок здесь жестко заданы, так как они представляют сами языки
def language_selection_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    uz_button = types.InlineKeyboardButton('🇺🇿 O\'zbek', callback_data='set_lang_uz')
    ru_button = types.InlineKeyboardButton('🇷🇺 Русский', callback_data='set_lang_ru')
    kb.add(uz_button, ru_button)
    return kb
