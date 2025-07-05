import telebot # Импортируем библиотеку PyTelegramBotAPI для создания бота
from telebot import types # Импортируем types для работы с клавиатурами
import buttons # Импортируем модуль buttons, предположительно содержащий функции для создания кнопок
import database # Импортируем модуль database, предположительно для работы с базой данных

# Создаем объект бота
# Замените 'YOUR_BOT_TOKEN' на ваш реальный токен бота
bot = telebot.TeleBot('***')

# Словарь для временного хранения данных пользователя во время регистрации
# Это позволяет передавать данные между шагами register_next_step_handler
user_registration_data = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # Проверяем юзера на наличие в БД
    if database.check_user(user_id):
        bot.send_message(user_id, 'Добро пожаловать!',
                         reply_markup=buttons.main_menu()) # Возвращаем основное меню, если пользователь уже зарегистрирован
    else:
        bot.send_message(user_id, 'Здравствуйте! Давайте начнем регистрацию!\n'
                                  'Напишите свое имя',
                         reply_markup=types.ReplyKeyboardRemove()) # Убираем любую кастомную клавиатуру
        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)

# Этап получения имени
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    # Сохраняем имя пользователя во временном хранилище
    user_registration_data[user_id] = {'name': user_name}

    bot.send_message(user_id, f'Отлично, {user_name}! Теперь отправьте свой номер телефона.',
                     reply_markup=buttons.num_button()) # Используем кнопку для отправки номера
    # Переход на этап получения номера
    bot.register_next_step_handler(message, get_num)

# Этап получения номера
def get_num(message):
    user_id = message.from_user.id
    # Проверяем, что сообщение содержит контакт
    if message.contact and message.contact.user_id == user_id:
        user_num = message.contact.phone_number
        # Сохраняем номер телефона во временном хранилище
        user_registration_data[user_id]['num'] = user_num

        bot.send_message(user_id, 'Спасибо за номер! Теперь, пожалуйста, отправьте вашу геолокацию.',
                         reply_markup=buttons.location_button()) # Используем кнопку для отправки геолокации
        # Переход на этап получения геолокации
        bot.register_next_step_handler(message, get_location)
    else:
        bot.send_message(user_id, 'Пожалуйста, используйте кнопку "Отправить номер телефона" для отправки контакта.')
        # Возвращаем на этап получения номера
        bot.register_next_step_handler(message, get_num)

# Этап получения геолокации
def get_location(message):
    user_id = message.from_user.id
    # Проверяем, что сообщение содержит геолокацию
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude

        # Получаем ранее сохраненные имя и номер из временного хранилища
        user_name = user_registration_data[user_id]['name']
        user_num = user_registration_data[user_id]['num']

        # Регистрируем пользователя в базе данных со всеми данными, включая геолокацию
        database.register(user_id, user_name, user_num, latitude, longitude)

        bot.send_message(user_id, 'Регистрация прошла успешно! Добро пожаловать!',
                         reply_markup=buttons.main_menu()) # Возвращаем основное меню
        # Очищаем временные данные пользователя после завершения регистрации
        if user_id in user_registration_data:
            del user_registration_data[user_id]
    else:
        bot.send_message(user_id, 'Пожалуйста, используйте кнопку "Отправить геолокацию" для отправки ваших координат.')
        # Возвращаем на этап получения геолокации
        bot.register_next_step_handler(message, get_location)


# Обработчик текстовых сообщений (остальной функционал бота)
@bot.message_handler(content_types=['text'])
def text(message):
    user_id = message.from_user.id
    # Проверяем, зарегистрирован ли пользователь, прежде чем обрабатывать другие команды
    if not database.check_user(user_id):
        bot.send_message(user_id, 'Пожалуйста, сначала завершите регистрацию, отправив /start.')
        return

    # Обработка кнопки "Мой профиль"
    if message.text.lower() == 'мой профиль':
        profile_data = database.get_user_profile(user_id)
        if profile_data:
            profile_text = (f"Ваш профиль:\n"
                            f"\nИмя: {profile_data['name']}\n"
                            f"\nНомер телефона: {profile_data['num']}\n"
                            f"\nГеолокация: "
                            f"\nШирота: {profile_data['latitude']}, "
                            f"\nДолгота: {profile_data['longitude']}")
            bot.send_message(user_id, profile_text, reply_markup=buttons.main_menu())
        else:
            bot.send_message(user_id, 'Не удалось найти данные вашего профиля. Пожалуйста, попробуйте зарегистрироваться снова (/start).',
                             reply_markup=buttons.main_menu())
    else: # Если сообщение не соответствует команде "Мой профиль"
        bot.send_message(user_id, 'Неизвестная команда. Пожалуйста, выберите действие из меню.', reply_markup=buttons.main_menu())


# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(non_stop=True)
