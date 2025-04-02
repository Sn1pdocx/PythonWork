import requests
import json

nbu_response = requests.get('https://bank.gov.ua/NBU_Exchange/exchange_site?start=20250324&end=20250328&valcode=usd&sort=exchangedate&order=desc&json')
print(nbu_response)
print(nbu_response.content)

converted_response = json.loads(nbu_response.content)
print(converted_response)

exchange_dates = []
exchange_rates = []

for item in converted_response:
    exchange_dates.append(item['exchangedate'])
    exchange_rates.append(item['rate'])

print(exchange_dates)
print(exchange_rates)

import matplotlib.pyplot as plt
plt.plot(exchange_dates, exchange_rates)
plt.show()