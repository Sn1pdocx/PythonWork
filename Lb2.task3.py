import re

def filter_ips(input_file_path, output_file_path, allowed_ips):
    ip_counts = {}

    try:
        #Читання вхідного лог-файлу
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                #Витягування IP-адресу на початку рядка
                match = re.match(r'^(\d{1,3}(?:\.\d{1,3}){3})', line)
                if match:
                    ip = match.group(1)
                    if ip in allowed_ips:
                        ip_counts[ip] = ip_counts.get(ip, 0) + 1

    except FileNotFoundError:
        print(f"[Помилка] Вхідний файл не знайдено: {input_file_path}")
        return
    except IOError as e:
        print(f"[Помилка читання файлу] {e}")
        return

    try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            print("Результати фільтрації дозволених IP-адрес:")
            for ip, count in ip_counts.items():
                line = f"{ip} - {count}"
                print(line)
                outfile.write(line + '\n')

    except IOError as e:
        print(f"[Помилка запису у файл] {output_file_path}: {e}")

if __name__ == "__main__":
    allowed_ips = ["200.49.190.101", "46.105.14.53", "54.255.13.204"]
    filter_ips("apache_logs.txt", "filtered_ips.txt", allowed_ips)
