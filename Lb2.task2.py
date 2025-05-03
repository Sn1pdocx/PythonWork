import hashlib

def generate_file_hashes(*file_paths):
    hashes = {}

    for path in file_paths:
        try:
            with open(path, 'rb') as file:
                sha256 = hashlib.sha256()
                while chunk := file.read(8192):  #Читаємо файл частинами
                    sha256.update(chunk)
                hashes[path] = sha256.hexdigest()
        except FileNotFoundError:
            print(f"[Помилка] Файл не знайдено: {path}")
        except IOError as e:
            print(f"[Помилка читання файлу] {path}: {e}")

    return hashes

if __name__ == "__main__":
    #Хеш для apache_logs.txt
    result = generate_file_hashes("apache_logs.txt")

    for file, file_hash in result.items():
        print(f"SHA-256 хеш для {file}:\n{file_hash}")
