import requests
from bs4 import BeautifulSoup
from check_connection import connection_proxy
import urllib.request
import urllib.parse
from datetime import datetime
import time
import re
import dateutil.relativedelta

proxy = connection_proxy()

def make_url(region_num, PriceFrom = '', PriceTo = ''):

    to_date = (datetime.today() - dateutil.relativedelta.relativedelta(days=3)).strftime('%d.%m.%Y')

    params = urllib.parse.urlencode(
        {'morphology': 'on', 'pageNumber': '1',
         'sortDirection': 'false', 'recordsPerPage': '_500',
         'showLotsInfoHidden': 'false', 'fz44': 'on', 'fz223': 'on', 'ppRf615': 'on', 'af': 'on', 'ca': 'on',
         'pc': 'on', 'pa': 'on', 'priceFrom' : PriceFrom, 'priceTo' : PriceTo, 'currencyId': '-1', 'regions': region_num, 'regionDeleted': 'false',
         'sortBy': 'UPDATE_DATE',
         'publishDateFrom': to_date})

    url = "http://zakupki.gov.ru/epz/order/quicksearch/search.html?%s" % params

    return url


def get_cities():

    cities = list()

    r = requests.get(
        'http://zakupki.gov.ru/epz/order/quicksearch/search.html#',
        headers=proxy[1], proxies=proxy[0])

    content = r.content.decode("utf8")

    if r.status_code == 200:

        soup = BeautifulSoup(content, 'html.parser')

        regions = soup.findAll("ul", {"id": "regionsTagDataContainer"})[0].findAll("label", {"class": "customCheckbox"})

        for region in regions:

            region_code = region.findAll('label')[0].get('for').split('_')[2]
            region_name = " ".join(region.get_text().split())

            cities.append([region_code, region_name])

    return cities


def get_records(city, PriceFrom = '', PriceTo = ''):

    records = 0
    big_records = 0

    url = make_url(city, PriceFrom, PriceTo)

    print (url)

    r = requests.get(url, headers=proxy[1], proxies=proxy[0])

    content = r.content.decode("utf8")

    soup = BeautifulSoup(content, 'html.parser')

    if r.status_code == 200 and "Поиск не дал результатов" not in content:

        raw_records = soup.findAll("p", {"class": "allRecords"})[0]
        records = raw_records.findAll("strong")[0].get_text()
        raw_records = raw_records.get_text()
        records = int("".join(re.findall(r'\d', records)))

        if records > 1000:
            records = int("".join(re.findall(r'\d', raw_records)))
            print (records)

    if records > 500:
        r = requests.get(url.replace("pageNumber=1", "pageNumber=2"), headers=proxy[1], proxies=proxy[0])
        content = content + r.content.decode("utf8")

    return records, content

if __name__ == "__main__":

    cities =  [['5277335', 'Москва'], ['5277327', 'Московская обл']]#get_cities()
    print (cities)

    for city in cities:
        result = get_records(city[0])
        records = result[0]

        if records < 1000:
            print("Записей по {} = {}".format(city[1], records))
            time.sleep(1)

        elif records > 1000:
            price_from = 3000000
            price_to = ''
            step = 500000

            while (price_from > 0):
                time.sleep(1)
                result =  get_records(city[0], PriceFrom=price_from-step, PriceTo= price_to)
                records2 = result[0]
                print("По региону {} диапазон от {} до {} записей = {}".format(city[1], price_from,price_to,  records2))

                if records2 < 1000:

                    price_to = price_from
                    price_from = price_from - step
                else:
                    step = step - 100000

