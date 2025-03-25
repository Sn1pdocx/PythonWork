import hashlib

user_data = {
    'login': 'user_Marginal',
    'password': hashlib.md5('Marginal_USA'.encode('utf-8')).hexdigest(),
    'full_name': 'Маргінал Анатолий Трампович'
}

def check_password():
    input_password = input("Введіть пароль: ")

    # Хешування паролю
    hashed_input = hashlib.md5(input_password.encode('utf-8')).hexdigest()

    #Перевірка зберігання в хеші
    if hashed_input == user_data['password']:
        print("Пароль вірний!")
    else:
        print("Невірний пароль!")

check_password()