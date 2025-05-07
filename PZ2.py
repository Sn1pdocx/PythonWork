import hashlib
from datetime import datetime


class User:
    def __init__(self, username: str, password: str = None, is_active: bool = True):
        self.username = username
        self.password_hash = self._hash_password(password) if password else None
        self.is_active = is_active

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verify_password(self, password: str) -> bool:
        if self.password_hash is None:
            return True
        return self.password_hash == self._hash_password(password)

    def __str__(self):
        return f"User(username='{self.username}', is_active={self.is_active})"


class Administrator(User):
    def __init__(self, username: str, password: str, is_active: bool = True):
        super().__init__(username, password, is_active)
        self.role = "Administrator"

    def __str__(self):
        return f"Administrator(username='{self.username}')"


class RegularUser(User):
    def __init__(self, username: str, password: str, is_active: bool = True):
        super().__init__(username, password, is_active)
        self.role = "RegularUser"
        self.last_login = None

    def update_last_login(self):
        self.last_login = datetime.now()

    def __str__(self):
        return f"RegularUser(username='{self.username}', last_login={self.last_login})"


class GuestUser(User):
    def __init__(self, username: str = "guest", is_active: bool = True):
        super().__init__(username, None, is_active)  # Без пароля
        self.role = "Guest"

    def __str__(self):
        return f"GuestUser(username='{self.username}')"


class AccessControl:
    def __init__(self):
        self.users = {}
        #Тестові користувачі
        self.add_user(Administrator("admin", "admin123"))
        self.add_user(RegularUser("user1", "password123"))
        self.add_user(GuestUser("guest"))

    def add_user(self, user: User) -> bool:
        if user.username in self.users:
            print(f"Користувач {user.username} вже існує!")
            return False
        self.users[user.username] = user
        print(f"Користувач {user.username} ({user.role}) успішно доданий")
        return True

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.users.get(username)
        if not user:
            print("Користувача не знайдено")
            return None
        if not user.is_active:
            print("Акаунт деактивовано")
            return None
        if not user.verify_password(password):
            print("Невірний пароль")
            return None
        if isinstance(user, RegularUser):
            user.update_last_login()
        print(f"Вітаємо, {username} ({user.role})!")
        return user

    def list_users(self):
        print("\nСписок користувачів:")
        for user in self.users.values():
            print(f"- {user}")


def display_user_types():
    print("\nТип користувача:")
    print("1. Адміністратор")
    print("2. Звичайний користувач")
    print("3. Гість")


def main():
    system = AccessControl()

    while True:
        print("\nГоловне меню:")
        print("1. Увійти в систему")
        print("2. Додати нового користувача")
        print("3. Переглянути список користувачів")
        print("4. Вийти")

        choice = input("Оберіть опцію: ")

        if choice == "1":
            username = input("Логін: ")
            password = input("Пароль: ")
            system.authenticate_user(username, password)

        elif choice == "2":
            display_user_types()
            user_type = input("Виберіть тип (1-3): ")

            username = input("Ім'я користувача: ")

            if user_type == "1":
                password = input("Пароль: ")
                system.add_user(Administrator(username, password))
            elif user_type == "2":
                password = input("Пароль: ")
                system.add_user(RegularUser(username, password))
            elif user_type == "3":
                system.add_user(GuestUser(username))
            else:
                print("Невірний вибір типу")

        elif choice == "3":
            system.list_users()

        elif choice == "4":
            print("До побачення!")
            break

        else:
            print("Невірний вибір")


if __name__ == "__main__":
    main()