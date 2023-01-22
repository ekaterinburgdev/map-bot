import requests
import re
from datetime import datetime

from okn import Okn

proxies = {
   'https': 'http://95.56.254.139:3128',
}

url = 'https://okn.midural.ru/spisok-pravovyh-aktov-sverdlovskoy-oblasti-o-vyyavlenii-obektov-kulturnogo-naslediya-prinyatye-v-2'

def parse_page() -> list[Okn]:
    response = requests.get(url, proxies=proxies)
    page = response.content.decode('utf-8')
    results = re.findall(r'<td>\w+<.+?\s<td><a href="(.+?)">.+\W<td>(.+?)<.+\s.+?td>(.+?)<br', page)
    return [Okn(result[1], 'https://okn.midural.ru' + result[0], datetime.strptime(result[2], '%d.%m.%Y').date()) for result in results]

def get_ekb_okns(okns: list[Okn]):
    for okn in okns:
        if 'объекта культурного наследия' in okn.name and 'г. Екатеринбург' in okn.name:
            yield okn
    
def get_orders_by_date(order_date) -> list[Okn]:
    all_okns = parse_page()
    ekb_okns = get_ekb_okns(all_okns)
    order_date_is_today = lambda okn: okn.date == order_date
    return list(filter(order_date_is_today, ekb_okns))
