import sqlite3 # Импортируем библиотеку sqlite3 для работы с базами данных SQLite

# Подключение к базе данных
# Устанавливаем соединение с базой данных 'delivery.db'.
# Если файл базы данных не существует, он будет создан.
# check_same_thread=False позволяет использовать соединение из разных потоков (полезно для ботов).
connection = sqlite3.connect('delivery.db', check_same_thread=False)
# Python + SQL
# Создаем объект курсора, который позволяет выполнять SQL-запросы к базе данных.
sql = connection.cursor()


# Создание таблицы пользователя
# Выполняем SQL-запрос для создания таблицы 'users' (пользователей).
# IF NOT EXISTS гарантирует, что таблица будет создана только если ее еще нет.
# Таблица содержит столбцы:
# tg_id (INTEGER) - ID пользователя Telegram
# name (TEXT) - имя пользователя
# num (TEXT) - номер телефона пользователя
# latitude (REAL) - широта геолокации пользователя (добавлено)
# longitude (REAL) - долгота геолокации пользователя (добавлено)
sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(tg_id INTEGER, name TEXT, num TEXT, latitude REAL, longitude REAL);')

# Создание таблицы продуктов
# Выполняем SQL-запрос для создания таблицы 'products' (продуктов).
# IF NOT EXISTS гарантирует, что таблица будет создана только если ее еще нет.
# Таблица содержит столбцы:
# pr_id (INTEGER PRIMARY KEY AUTOINCREMENT) - уникальный ID продукта, автоматически увеличивающийся
# pr_name (TEXT) - название продукта
# pr_des (TEXT) - описание продукта
# pr_count (INTEGER) - количество продукта на складе
# pr_price (INTEGER) - цена продукта (может быть десятичным числом)
# pr_photo (TEXT) - путь к фотографии продукта или URL
sql.execute('CREATE TABLE IF NOT EXISTS products '
            '(pr_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'pr_name TEXT, pr_des TEXT, pr_count INTEGER, '
            'pr_price INTEGER, pr_photo TEXT);')

# Создание таблицы корзины
# Выполняем SQL-запрос для создания таблицы 'cart' (корзины).
# IF NOT EXISTS гарантирует, что таблица будет создана только если ее еще нет.
# Таблица содержит столбцы:
# user_id (INTEGER) - ID пользователя, которому принадлежит корзина
# user_product (TEXT) - название продукта в корзине
# user_pr_amount (INTEGER) - количество данного продукта в корзине пользователя
sql.execute('CREATE TABLE IF NOT EXISTS cart '
            '(user_id INTEGER, user_product TEXT, '
            'user_pr_amount INTEGER);')


## Методы пользователя ##
# Регистрация
# Определяем функцию register для добавления нового пользователя в таблицу 'users'.
# Теперь функция принимает также latitude и longitude.
def register(tg_id, name, num, latitude=None, longitude=None):
    # Выполняем SQL-запрос для вставки новой записи в таблицу 'users'.
    # Добавлены плейсхолдеры для latitude и longitude.
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?);',
                (tg_id, name, num, latitude, longitude))
    # Фиксация изменений
    # Сохраняем (коммитим) все изменения, сделанные в базе данных, чтобы они стали постоянными.
    connection.commit()


# Проверка на наличие пользователя в БД
# Определяем функцию check_user для проверки, существует ли пользователь в таблице 'users'.
def check_user(tg_id):
    # Выполняем SQL-запрос для выбора всех столбцов из таблицы 'users',
    # где tg_id совпадает с переданным значением.
    # .fetchone() извлекает первую найденную строку или None, если строк нет.
    if sql.execute('SELECT * FROM users WHERE tg_id=?;', (tg_id,)).fetchone():
        return True # Возвращаем True, если пользователь найден
    else:
        return False # Возвращаем False, если пользователь не найден

# Функция для получения данных профиля пользователя
def get_user_profile(tg_id):
    # Выбираем имя, номер, широту и долготу для данного пользователя
    result = sql.execute('SELECT name, num, latitude, longitude FROM users WHERE tg_id=?;', (tg_id,)).fetchone()
    if result:
        # Возвращаем данные в виде словаря для удобства
        return {
            'name': result[0],
            'num': result[1],
            'latitude': result[2],
            'longitude': result[3]
        }
    else:
        return None # Возвращаем None, если пользователь не найден

# Функция get_user_location была удалена, так как она больше не используется.
