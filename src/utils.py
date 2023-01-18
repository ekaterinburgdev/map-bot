import requests
import re
from datetime import datetime

from okn import Okn


def parse_page() -> list[Okn]:
    response = requests.get('https://okn.midural.ru/spisok-pravovyh-aktov-sverdlovskoy-oblasti-o-vyyavlenii-obektov-kulturnogo-naslediya-prinyatye-v-2')
    page = response.content.decode('utf-8')
    results = re.findall(r'<td>\w+<.+?\s<td><a href="(.+?)">.+\W<td>(.+?)<.+\s.+?td>(.+?)<br', page)
    return [Okn(result[1], 'https://okn.midural.ru' + result[0], datetime.strptime(result[2], '%d.%m.%Y').date()) for result in results]
    
def get_orders_by_date(order_date) -> list[Okn]:
    okns = parse_page()
    order_date_is_today = lambda okn: okn.date == order_date
    return list(filter(order_date_is_today, okns))
