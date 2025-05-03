import re

def analyze_log_file(log_file_path):
    response_codes = {}

    try:
        #Читання з кодуванням UTF-8
        with open(log_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                #Шукаємо HTTP-код відповіді за допомогою регулярного виразу
                match = re.search(r'"\s(\d{3})\s', line)
                if match:
                    code = match.group(1)
                    response_codes[code] = response_codes.get(code, 0) + 1

    except FileNotFoundError:
        print(f"[Помилка] Файл не знайдено: {log_file_path}")

    except IOError as e:
        print(f"[Помилка читання файлу] {e}")

    #Повернення словника
    return response_codes

if __name__ == "__main__":
    path = "apache_logs.txt"
    results = analyze_log_file(path)

    #Якщо є результати — виводимо кожен код і скільки разів він зустрічається
    if results:
        print("Коди відповідей HTTP та їх кількість:")
        for code, count in results.items():
            print(f"{code}: {count}")
    else:
        print("Файл оброблено, але не знайдено кодів або файл порожній.")
