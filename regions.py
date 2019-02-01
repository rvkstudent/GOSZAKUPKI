import requests
from bs4 import BeautifulSoup

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
    'http://zakupki.gov.ru/epz/order/quicksearch/search.html#',
    headers=headers, proxies=proxies)


content = r.content.decode("utf8")

print (r.status_code)


soup = BeautifulSoup(content, 'html.parser')

#print(soup.prettify())


regions = soup.findAll("ul", {"id": "regionsTagDataContainer"})[0].findAll("label", {"class": "customCheckbox"})

for region in regions:
    print (region.findAll('label')[0].get('for').split('_')[2])
    print(" ".join(region.get_text().split()))
