import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from datetime import datetime

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

proxies = {'http': 'http://kozlov.r:Fvcnthlfv2019@10.77.20.61:3128/'}



r = requests.get(
    'http://zakupki.gov.ru/epz/order/quicksearch/search.html?morphology=on&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&fz44=on&fz223=on&ppRf615=on&af=on&ca=on&pc=on&pa=on&currencyId=-1&regionDeleted=false&sortBy=PUBLISH_DATE',
    headers=headers, proxies=proxies)



content = r.content.decode("utf8")

print (r.status_code)


soup = BeautifulSoup(content, 'html.parser')

#print(soup.prettify())


tenders = soup.findAll("div", {"class": "registerBox registerBoxBank margBtm20"})

print ("Тендеров нашлось: {}".format (len(tenders)))

for tender in tenders:

    auction_type = ""
    zakup_status = ""
    zakup_zakon = ""
    price = 0
    procedure_num = ""
    razmesheno = ""
    oraganisation = ""
    obnovleno = ""

    tenderTds = tender.findAll("td", {"class": "tenderTd"})
    for tenderTd in tenderTds:

        dts = tenderTd.findAll("dt")
        auction_type = dts[0].get_text().strip(' \t\n')
        zakup_status = " ".join(dts[1].get_text().split('/')[0].split())
        zakup_zakon = dts[1].get_text().split()[3]
        price_text = tenderTd.findAll("dd")[1].findAll("strong")
        if len(price_text) > 0:
            price = "".join(price_text[0].get_text().split())


    descriptTenderTd = tender.findAll("td", {"class": "descriptTenderTd"})[0]

    dts = descriptTenderTd.findAll("dt")
    procedure_num  = dts[0].get_text().split()[1]

    oraganisation = " ".join(descriptTenderTd.findAll("dd", {"class": "nameOrganization"})[0].get_text().split()).replace("Заказчик: ", "")

    description = " ".join(
        descriptTenderTd.findAll("dd")[1].get_text().split())

    amountTenderTds = tender.findAll("td", {"class": "amountTenderTd"})

    for amountTenderTd in amountTenderTds:
        lis = amountTenderTd.findAll("li")

        razmesheno = " ".join(lis[0].get_text().split()).replace("Размещено: ", "")
        obnovleno = " ".join(lis[1].get_text().split()).replace("Обновлено: ", "")

    print ("Тип аукциона: {}".format(auction_type))
    print("Статус закупки: {}".format(zakup_status))
    print("Закон: {}".format(zakup_zakon))
    print("Начальная цена: {}".format(price))
    print("Номер процедуры: {}".format(procedure_num))
    print("Заказчик: {}".format(oraganisation))
    print("Размещено: {}".format(razmesheno))
    print("Обновлено: {}".format(obnovleno))
    print("Описание: {}".format(description))

    pg_price = price.replace(',','.')

    split_date = razmesheno.split('.')
    pg_created = "{}-{}-{}".format(split_date[2], split_date[1], split_date[0])
    split_date = obnovleno.split('.')
    pg_modified = "{}-{}-{}".format(split_date[2], split_date[1], split_date[0])

    print (pg_created)

#if ("Соболевского" in content):
#    print(content)