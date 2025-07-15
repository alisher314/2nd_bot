import telebot
from telebot import types
import buttons
import database

# Создаем объект бота
bot = telebot.TeleBot('***') # Замените на ваш реальный токен

# Словарь для временного хранения данных пользователя во время регистрации
user_registration_data = {}

# --- Словарь для локализации текстов ---
MESSAGES = {
    'ru': {
        'welcome': 'Добро пожаловать!',
        'register_start': 'Здравствуйте! Давайте начнем регистрацию!\nНапишите свое имя',
        'send_number_prompt': 'Отлично, {name}! Теперь отправьте свой номер телефона.',
        'send_number_button': 'Отправить номер📞',
        'send_contact_error': 'Пожалуйста, используйте кнопку "Отправить номер телефона" для отправки контакта.',
        'send_location_prompt': 'Спасибо за номер! Теперь, пожалуйста, отправьте вашу геолокацию.',
        'send_location_button': 'Отправить геолокацию📍',
        'send_location_error': 'Пожалуйста, используйте кнопку "Отправить геолокацию" для отправки ваших координат.',
        'registration_success': 'Регистрация прошла успешно! Добро пожаловать!',
        'registration_needed': 'Пожалуйста, сначала завершите регистрацию, отправив /start.',
        'my_profile_button': 'Мой профиль',
        'settings_button': 'Настройки',
        'change_lang_button': 'Изменить язык',
        'back_to_main_button': 'Назад в главное меню',
        'profile_header': 'Ваш профиль:',
        'name_label': 'Имя',
        'phone_label': 'Номер телефона',
        'location_label': 'Геолокация',
        'latitude_label': 'Широта',
        'longitude_label': 'Долгота',
        'language_label': 'Язык',
        'profile_not_found': 'Не удалось найти данные вашего профиля. Пожалуйста, попробуйте зарегистрироваться снова (/start).',
        'choose_settings_action': 'Выберите действие в настройках:',
        'choose_language': 'Выберите язык:',
        'lang_changed_ru_msg': 'Язык изменен на Русский.',
        'lang_changed_uz_msg': 'Til O\'zbek tiliga o\'zgartirildi.',
        'lang_changed_success_callback': 'Язык успешно изменен!',
        'main_menu_return': 'Вы вернулись в главное меню.',
        'unknown_command': 'Неизвестная команда. Пожалуйста, выберите действие из меню.',
        'lang_ru_name': 'Русский',
        'lang_uz_name': 'Узбекский'
    },
    'uz': {
        'welcome': 'Xush kelibsiz!',
        'register_start': 'Assalomu alaykum! Ro\'yxatdan o\'tishni boshlaymiz!\nIsmingizni kiriting',
        'send_number_prompt': 'Ajoyib, {name}! Endi telefon raqamingizni yuboring.',
        'send_number_button': 'Raqamni yuborish📞',
        'send_contact_error': 'Iltimos, kontaktni yuborish uchun "Telefon raqamini yuborish" tugmasidan foydalaning.',
        'send_location_prompt': 'Raqamingiz uchun rahmat! Endi joylashuvingizni yuboring.',
        'send_location_button': 'Joylashuvni yuborish📍',
        'send_location_error': 'Iltimos, joylashuvingizni yuborish uchun "Joylashuvni yuborish" tugmasidan foydalaning.',
        'registration_success': 'Ro\'yxatdan o\'tish muvaffaqiyatli yakunlandi! Xush kelibsiz!',
        'registration_needed': 'Iltimos, avval /start buyrug\'ini yuborib ro\'yxatdan o\'ting.',
        'my_profile_button': 'Mening profilim',
        'settings_button': 'Sozlamalar',
        'change_lang_button': 'Tilni o\'zgartirish',
        'back_to_main_button': 'Bosh menyuga qaytish',
        'profile_header': 'Sizning profilingiz:',
        'name_label': 'Ism',
        'phone_label': 'Telefon raqami',
        'location_label': 'Joylashuv',
        'latitude_label': 'Kenglik',
        'longitude_label': 'Uzunlik',
        'language_label': 'Til',
        'profile_not_found': 'Profil ma\'lumotlaringiz topilmadi. Iltimos, /start orqali qayta ro\'yxatdan o\'tishga urinib ko\'ring.',
        'choose_settings_action': 'Sozlamalarda harakatni tanlang:',
        'choose_language': 'Tilni tanlang:',
        'lang_changed_ru_msg': 'Til Rus tiliga o\'zgartirildi.',
        'lang_changed_uz_msg': 'Til O\'zbek tiliga o\'zgartirildi.',
        'lang_changed_success_callback': 'Til muvaffaqiyatli o\'zgartirildi!',
        'main_menu_return': 'Siz bosh menyuga qaytdingiz.',
        'unknown_command': 'Noma\'lum buyruq. Iltimos, menyudan harakatni tanlang.',
        'lang_ru_name': 'Rus tili',
        'lang_uz_name': 'O\'zbek tili'
    }
}

# Вспомогательная функция для получения языка пользователя
def get_user_language(user_id):
    profile = database.get_user_profile(user_id)
    if profile and profile['language']:
        return profile['language']
    return 'ru' # Язык по умолчанию, если пользователь не найден или язык не установлен

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_lang = get_user_language(user_id) # Получаем язык пользователя

    if database.check_user(user_id):
        bot.send_message(user_id, MESSAGES[user_lang]['welcome'],
                         reply_markup=buttons.main_menu(MESSAGES, user_lang))
    else:
        bot.send_message(user_id, MESSAGES[user_lang]['register_start'],
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name)

# Этап получения имени
def get_name(message):
    user_id = message.from_user.id
    user_lang = get_user_language(user_id)
    user_name = message.text
    user_registration_data[user_id] = {'name': user_name}

    bot.send_message(user_id, MESSAGES[user_lang]['send_number_prompt'].format(name=user_name),
                     reply_markup=buttons.num_button(MESSAGES, user_lang))
    bot.register_next_step_handler(message, get_num)

# Этап получения номера
def get_num(message):
    user_id = message.from_user.id
    user_lang = get_user_language(user_id)

    if message.contact and message.contact.user_id == user_id:
        user_num = message.contact.phone_number
        user_registration_data[user_id]['num'] = user_num

        bot.send_message(user_id, MESSAGES[user_lang]['send_location_prompt'],
                         reply_markup=buttons.location_button(MESSAGES, user_lang))
        bot.register_next_step_handler(message, get_location)
    else:
        bot.send_message(user_id, MESSAGES[user_lang]['send_contact_error'])
        bot.register_next_step_handler(message, get_num)

# Этап получения геолокации
def get_location(message):
    user_id = message.from_user.id
    user_lang = get_user_language(user_id) # Используем язык по умолчанию или ранее сохраненный

    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude

        user_name = user_registration_data[user_id]['name']
        user_num = user_registration_data[user_id]['num']

        # При регистрации нового пользователя сохраняем язык по умолчанию 'ru'
        # или можно передать язык, если бы выбор языка был на первом шаге
        database.register(user_id, user_name, user_num, latitude, longitude, language='ru')

        bot.send_message(user_id, MESSAGES[user_lang]['registration_success'],
                         reply_markup=buttons.main_menu(MESSAGES, user_lang))
        if user_id in user_registration_data:
            del user_registration_data[user_id]
    else:
        bot.send_message(user_id, MESSAGES[user_lang]['send_location_error'])
        bot.register_next_step_handler(message, get_location)


# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def text(message):
    user_id = message.from_user.id
    user_lang = get_user_language(user_id) # Получаем язык пользователя

    if not database.check_user(user_id):
        bot.send_message(user_id, MESSAGES[user_lang]['registration_needed'])
        return

    # Обработка кнопок на основе их локализованного текста
    if message.text == MESSAGES[user_lang]['my_profile_button']:
        profile_data = database.get_user_profile(user_id)
        if profile_data:
            # Используем локализованные метки для профиля
            profile_text = (f"{MESSAGES[user_lang]['profile_header']}\n"
                            f"\n{MESSAGES[user_lang]['name_label']}: {profile_data['name']}\n"
                            f"\n{MESSAGES[user_lang]['phone_label']}: {profile_data['num']}\n"
                            f"\n{MESSAGES[user_lang]['location_label']}: "
                            f"\n  {MESSAGES[user_lang]['latitude_label']}: {profile_data['latitude']}\n"
                            f"\n  {MESSAGES[user_lang]['longitude_label']}: {profile_data['longitude']}\n"
                            f"\n{MESSAGES[user_lang]['language_label']}: {MESSAGES[user_lang]['lang_uz_name'] if profile_data['language'] == 'uz' else MESSAGES[user_lang]['lang_ru_name']}")
            bot.send_message(user_id, profile_text, reply_markup=buttons.main_menu(MESSAGES, user_lang))
        else:
            bot.send_message(user_id, MESSAGES[user_lang]['profile_not_found'],
                             reply_markup=buttons.main_menu(MESSAGES, user_lang))

    elif message.text == MESSAGES[user_lang]['settings_button']:
        bot.send_message(user_id, MESSAGES[user_lang]['choose_settings_action'],
                         reply_markup=buttons.settings_menu(MESSAGES, user_lang))

    elif message.text == MESSAGES[user_lang]['change_lang_button']:
        bot.send_message(user_id, MESSAGES[user_lang]['choose_language'],
                         reply_markup=buttons.language_selection_menu()) # Это InlineKeyboard

    elif message.text == MESSAGES[user_lang]['back_to_main_button']:
        bot.send_message(user_id, MESSAGES[user_lang]['main_menu_return'],
                         reply_markup=buttons.main_menu(MESSAGES, user_lang))
    else:
        bot.send_message(user_id, MESSAGES[user_lang]['unknown_command'], reply_markup=buttons.main_menu(MESSAGES, user_lang))

# Обработчик для Inline-кнопок (выбор языка)
@bot.callback_query_handler(func=lambda call: call.data.startswith('set_lang_'))
def callback_inline_language(call):
    user_id = call.from_user.id
    language_code = call.data.split('_')[2] # Получаем 'uz' или 'ru'

    database.update_user_language(user_id, language_code) # Обновляем язык в БД

    # Обновляем user_lang, чтобы следующие сообщения были на новом языке
    user_lang = language_code

    if language_code == 'ru':
        # Редактируем сообщение, которое содержало inline-клавиатуру
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=MESSAGES[user_lang]['lang_changed_ru_msg'],
                              reply_markup=None) # Убираем инлайн-клавиатуру
    elif language_code == 'uz':
        # Редактируем сообщение, которое содержало inline-клавиатуру
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=MESSAGES[user_lang]['lang_changed_uz_msg'],
                              reply_markup=None) # Убираем инлайн-клавиатуру

    # Отправляем главное меню на новом языке
    bot.send_message(user_id, MESSAGES[user_lang]['welcome'], reply_markup=buttons.main_menu(MESSAGES, user_lang))

    bot.answer_callback_query(call.id, text=MESSAGES[user_lang]['lang_changed_success_callback'])


# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(non_stop=True)
