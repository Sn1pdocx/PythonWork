sales = [
    {"продукт": "яблука", "кількість": 50, "ціна": 20},
    {"продукт": "банани", "кількість": 30, "ціна": 25},
    {"продукт": "молоко", "кількість": 40, "ціна": 30},
    {"продукт": "хліб", "кількість": 20, "ціна": 15},
    {"продукт": "яйця", "кількість": 100, "ціна": 12},
    {"продукт": "яблука", "кількість": 60, "ціна": 20},
    {"продукт": "молоко", "кількість": 30, "ціна": 30}
]

def calculate_revenue(sales_list):

    revenue = {}

    for sale in sales_list:
        product = sale["продукт"]
        total_price = sale["кількість"] * sale["ціна"]

        if product in revenue:
            revenue[product] += total_price
        else:
            revenue[product] = total_price

    return revenue

#загальний дохід
total_revenue = calculate_revenue(sales)

#список продуктів, що принесли дохід більше 1000
high_revenue_products = [product for product, income in total_revenue.items() if income > 1000]

print("Загальний дохід по продуктах:", total_revenue)
print("Продукти з доходом більше 1000:", high_revenue_products)
