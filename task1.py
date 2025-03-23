def count_words(text):
    words = text.lower().split()

    #словник
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

text = "bibizyan its fun. bibizyan its cool. bibizyan its awesome. bibizyan its wow"
word_count = count_words(text)
print("Частота слів:", word_count)
