# Початковий словник продуктів на складі
stock = {
    "яблука": 10,
    "банани": 3,
    "молоко": 7,
    "хліб": 2,
    "яйця": 12
}

def update_stock(product, quantity):
    if product in stock:
        stock[product] += quantity
        if stock[product] < 0:
            stock[product] = 0  # Не дозволяємо від'ємні значення
    else:
        if quantity > 0:
            stock[product] = quantity  # Додаємо новий товар

    print(f"Оновлено: {product} = {stock[product]} шт.")

update_stock("банани", 2)  # Додаємо 2 банани
update_stock("хліб", -1)  # Видаляємо 1 хліб
update_stock("сік", 5)  # Додаємо новий товар "сік"

#список продуктів, яких менше ніж 5
low_stock_items = [product for product, count in stock.items() if count < 5]

print("Оновлений склад:", stock)
print("Продукти з кількістю менше 5:", low_stock_items)
