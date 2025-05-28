import sqlite3
import hashlib

#Підключення до БД (файл 'database.db')
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

#Створення таблиці в БД,якщо її немає
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        login TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL
    )
''')
connection.commit()
connection.close()

#Повернення SHA-256 хеш від пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#Перевірка на мінімальну довжину пароля
def password_is_valid(password):
    return len(password) >= 6

#Додавання нового користувача до БД
def add_user(login, password, full_name):
    if not password_is_valid(password):
        print("Пароль занадто короткий. Мінімум 6 символів.")
        return
    hashed = hash_password(password)
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (login, password, full_name) VALUES (?, ?, ?)',
                           (login, hashed, full_name))
            conn.commit()
        print("Користувача додано.")
    except sqlite3.IntegrityError:
        print("Користувач з таким логіном вже існує.")

#Оновлення пароля для існуючого користувача
def update_password(login, new_password):
    if not password_is_valid(new_password):
        print("Пароль занадто короткий. Мінімум 6 символів.")
        return
    hashed = hash_password(new_password)
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET password = ? WHERE login = ?', (hashed, login))
        if cursor.rowcount == 0:
            print("Користувача не знайдено.")
        else:
            print("Пароль оновлено.")
        conn.commit()

#Видалення користувача з бази за логіном
def delete_user(login):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE login = ?', (login,))
        if cursor.rowcount == 0:
            print("Користувача не знайдено.")
        else:
            print("Користувача видалено.")
        conn.commit()

#Перевірка автентифікації користувача (логін + пароль)
def authenticate(login, password):
    hashed = hash_password(password)
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, hashed))
        result = cursor.fetchone()
        if result:
            print(f"Успішна автентифікація. Ласкаво просимо, {result[2]}!")
        else:
            print("Невірний логін або пароль.")
#Меню
def main():
    while True:
        print("\nОберіть дію:")
        print("1. Додати користувача")
        print("2. Оновити пароль")
        print("3. Перевірка автентифікації")
        print("4. Видалити користувача")
        print("5. Вихід")
        choice = input("Ваш вибір: ")

        if choice == '1':
            login = input("Логін: ")
            full_name = input("ПІБ: ")
            password = input("Пароль: ")
            add_user(login, password, full_name)

        elif choice == '2':
            login = input("Логін: ")
            new_password = input("Новий пароль: ")
            update_password(login, new_password)

        elif choice == '3':
            login = input("Логін: ")
            password = input("Пароль: ")
            authenticate(login, password)

        elif choice == '4':
            login = input("Логін користувача, якого видалити: ")
            delete_user(login)

        elif choice == '5':
            print("Завершення програми.")
            break

        else:
            print("Невірний вибір.")

# Запуск програми
if __name__ == "__main__":
    main()
