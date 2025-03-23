def count_words(text):
    # Розділяємо рядок на слова та приводимо до нижнього регістру для коректного підрахунку
    words = text.lower().split()

    #словник для підрахунку частоти кожного слова
    word_count = {}

    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    #список слів, що зустрічаються більше трьох разів
    frequent_words = [word for word, count in word_count.items() if count > 3]

    print("Слова, що зустрічаються більше трьох разів:", frequent_words)

    return word_count

text = "bibizyan is cool. bibizyan is awesome. bibizyan is wow. bibizyan is fun."
word_count = count_words(text)
print("Частота слів:", word_count)
