import sqlite3
from datetime import datetime, timedelta
import os

DB_FILE = 'table_events.db'

#Ініціалізація бази даних
def init_db():
    first_run = not os.path.exists(DB_FILE)
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        #Створення таблиці джерел подій
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS EventSources (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            location TEXT,
            type TEXT
        )
        ''')

        #Створення таблиці типів подій
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS EventTypes (
            id INTEGER PRIMARY KEY,
            type_name TEXT UNIQUE,
            severity TEXT
        )
        ''')
        #Створення таблиці подій безпеки
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS SecurityEvents (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME,
            source_id INTEGER,
            event_type_id INTEGER,
            message TEXT,
            ip_address TEXT,
            username TEXT,
            FOREIGN KEY (source_id) REFERENCES EventSources(id),
            FOREIGN KEY (event_type_id) REFERENCES EventTypes(id)
        )
        ''')
        #Якщо це перший запуск,то додаємо стандартні типи подій
        if first_run:
            event_types = [
                ("Login Success", "Informational"),
                ("Login Failed", "Warning"),
                ("Port Scan Detected", "Warning"),
                ("Malware Alert", "Critical")
            ]
            cursor.executemany('''
            INSERT OR IGNORE INTO EventTypes (type_name, severity) VALUES (?, ?)
            ''', event_types)

        conn.commit()

#Функції
#Додавання нового джерела
def register_event_source(name, location, type_):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            INSERT OR IGNORE INTO EventSources (name, location, type) VALUES (?, ?, ?)
        ''', (name, location, type_))
        conn.commit()
        print("Джерело подій додано.")

#Додавання нового типу подій
def register_event_type(type_name, severity):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            INSERT OR IGNORE INTO EventTypes (type_name, severity) VALUES (?, ?)
        ''', (type_name, severity))
        conn.commit()
        print("Тип події додано.")

#Регестрація нової події безпеки
def log_security_event(source_name, event_type_name, message, ip_address=None, username=None):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        #Отримуємо ID джерела події
        cursor.execute('SELECT id FROM EventSources WHERE name = ?', (source_name,))
        source_id = cursor.fetchone()
        #Отримуємо ID типу події
        cursor.execute('SELECT id FROM EventTypes WHERE type_name = ?', (event_type_name,))
        event_type_id = cursor.fetchone()

        if not source_id or not event_type_id:
            print("Invalid source or event type.")
            return

        #Поточна дата і час
        timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
        #Додавання події
        cursor.execute('''
            INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, source_id[0], event_type_id[0], message, ip_address, username))
        conn.commit()
        print("Подію зареєстровано.")

#Запити
#Події 'Login Failed' за останні 24 години
def get_login_failed_last_24h():
    with sqlite3.connect(DB_FILE) as conn:
        since = (datetime.now() - timedelta(days=1)).isoformat(sep=' ', timespec='seconds')
        result = conn.execute('''
            SELECT * FROM SecurityEvents
            WHERE event_type_id = (SELECT id FROM EventTypes WHERE type_name = 'Login Failed')
            AND timestamp >= ?
        ''', (since,)).fetchall()
        return result

#Виявлення підбору пароля — більше 5 невдалих входів з однієї IP за годину
def detect_brute_force():
    with sqlite3.connect(DB_FILE) as conn:
        result = conn.execute('''
            SELECT ip_address, COUNT(*) as attempts, MIN(timestamp), MAX(timestamp)
            FROM SecurityEvents
            WHERE event_type_id = (SELECT id FROM EventTypes WHERE type_name = 'Login Failed')
            AND ip_address IS NOT NULL
            GROUP BY ip_address, strftime('%Y-%m-%d %H', timestamp)
            HAVING attempts > 5
        ''').fetchall()
        return result
#Критичні події за останній тиждень, згруповані за джерелом
def get_critical_events_last_week():
    with sqlite3.connect(DB_FILE) as conn:
        since = (datetime.now() - timedelta(days=7)).isoformat(sep=' ', timespec='seconds')
        result = conn.execute('''
            SELECT E.timestamp, S.name, T.type_name, E.message
            FROM SecurityEvents E
            JOIN EventSources S ON E.source_id = S.id
            JOIN EventTypes T ON E.event_type_id = T.id
            WHERE T.severity = 'Critical'
            AND E.timestamp >= ?
            ORDER BY S.name
        ''', (since,)).fetchall()
        return result
#Пошук подій за ключовим словом у повідомленні
def search_events_by_keyword(keyword):
    with sqlite3.connect(DB_FILE) as conn:
        result = conn.execute('''
            SELECT * FROM SecurityEvents
            WHERE message LIKE ?
        ''', (f'%{keyword}%',)).fetchall()
        return result

#Меню
def main():
    while True:
        print("\n--- Меню ---")
        print("1. Додати нове джерело подій")
        print("2. Додати новий тип події")
        print("3. Зареєструвати нову подію безпеки")
        print("4. Події 'Login Failed' за останні 24 години")
        print("5. IP з більш ніж 5 невдалими входами за 1 годину")
        print("6. 'Critical' події за останній тиждень")
        print("7. Пошук подій за ключовим словом")
        print("0. Вихід")

        match input("Оберіть опцію: "):
            case '1':
                name = input("Назва джерела: ")
                location = input("Локація/IP: ")
                type_ = input("Тип: ")
                register_event_source(name, location, type_)
            case '2':
                type_name = input("Назва типу події: ")
                severity = input("Рівень серйозності: ")
                register_event_type(type_name, severity)
            case '3':
                source = input("Назва джерела: ")
                event_type = input("Тип події: ")
                message = input("Повідомлення: ")
                ip = input("IP-адреса (необов’язково): ") or None
                user = input("Ім’я користувача (необов’язково): ") or None
                log_security_event(source, event_type, message, ip, user)
            case '4':
                events = get_login_failed_last_24h()
                for e in events:
                    print(e)
            case '5':
                brute_force = detect_brute_force()
                for bf in brute_force:
                    print(bf)
            case '6':
                critical = get_critical_events_last_week()
                for c in critical:
                    print(c)
            case '7':
                kw = input("Ключове слово: ")
                results = search_events_by_keyword(kw)
                for r in results:
                    print(r)
            case '0':
                print("Вихід...")
                break
            case _:
                print("Невірна опція")

if __name__ == "__main__":
    init_db()
    main()
