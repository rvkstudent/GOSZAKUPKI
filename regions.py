# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
#from check_connection import connection_proxy
import urllib.request
import urllib.parse
from datetime import datetime
import time
import re
import dateutil.relativedelta
from analise import find_tenders_info

#proxy = connection_proxy()

def request_url(url):

    headers  = {"Host": "zakupki.gov.ru",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "http://zakupki.gov.ru/epz/main/public/home.html",
    "Connection": "keep-alive",
    "Cookie": "routeepz7=1; routeepz0=3; routeepz2=0; _ym_uid=154858942172065130; _ym_d=1548589421; _ym_isad=2",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0"}

    proxy = {'http': 'http://95.213.229.42:80/'}

    r = requests.get(url, headers=headers, proxies= proxy)

    if (r.status_code != 200):
        print ("Статус код неверный: {}".format(r.status_code))

    return r


def make_url(region_num, PriceFrom = '', PriceTo = ''):

    to_date = (datetime.today() - dateutil.relativedelta.relativedelta(days=5)).strftime('%d.%m.%Y')

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

    r = request_url('http://zakupki.gov.ru/epz/order/quicksearch/search.html#')

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

    #print (url)

    r = request_url(url)

    content = r.content.decode("utf8")

    soup = BeautifulSoup(content, 'html.parser')

    if r.status_code == 200 and "Поиск не дал результатов" not in content:

        raw_records = soup.findAll("p", {"class": "allRecords"})[0]
        records = raw_records.findAll("strong")[0].get_text()
        raw_records = raw_records.contents
        records = int("".join(re.findall(r'\d', records)))

        if records >= 1000:

            records = int("".join(re.findall(r'\d', raw_records[2])))

            print ("Больше тысячи: {}".format(records))

    if records > 500:
        r = request_url(url.replace("pageNumber=1", "pageNumber=2"))
        content = content + r.content.decode("utf8")

    return records, content

if __name__ == "__main__":

    cities = get_cities() #[['5277335', 'Москва'], ['5277327', 'Московская обл']]#

    print("Время начала: {}".format(datetime.today()))

    total_tenders_count = 0

    result = get_records('')
    records_ishodnoe = result[0]

    print("Всего тендеров по порталу: {}".format(records_ishodnoe))

    for city in cities:

        result = get_records(city[0])
        records = result[0]

        if records < 1000:
            print("Записей по {} = {}".format(city[1], records))
            time.sleep(1)
            total_tenders_count = total_tenders_count + records

        elif records > 1000:
            price_from = 10000000
            price_to = ''
            step = 500000
            total_records = 0

            while (price_from > 0):
                time.sleep(5)
                price_from = price_from - step

                if price_from <= 0:
                    price_from = 0

                result =  get_records(city[0], PriceFrom=price_from, PriceTo= price_to)
                records2 = result[0]



                if records2 < 1000:

                    print("По региону {} диапазон от {} до {} записей = {}".format(city[1], price_from, price_to,
                                                                                   records2))
                    price_to = price_from-1
                    total_records = total_records + records2
                    find_tenders_info(result[1])
                    total_tenders_count = total_tenders_count + records2


                else:
                    price_from = price_from + step
                    step = step - 100000


            print ("Итого записей: {}".format(total_records))


    print("Время окончания: {}".format(datetime.today()))
    print("Итого тендеров собрано: {} из {}".format(total_records, records_ishodnoe))
