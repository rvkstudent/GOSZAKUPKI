import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

proxy_list = list()

url = "https://hidemyna.me/ru/proxy-list/?country=RU&maxtime=200&type=h#list"

options = Options()
options.add_argument('--headless')

driver = webdriver.Firefox(options=options)

driver.get(url)

try:
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'proxy__t')))
except TimeoutException:
    has_protocols = False
finally:
    print('No exception')

content = driver.find_element_by_class_name('proxy__t').get_attribute("outerHTML")

driver.close()

print(content)

soup = BeautifulSoup(content, 'html.parser')

proxies_rows = soup.findAll("tbody")[0].findAll("tr")

for tr in proxies_rows:
    proxy_ip = tr.findAll("td")[0].get_text()
    proxy_port = tr.findAll("td")[1].get_text()

    proxy_list.append([proxy_ip,proxy_port])

#print (proxy_list)

working_proxy = list()
best_proxy = list()

for proxy in proxy_list:

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

    proxy = {'http': 'http://{}:{}/'.format(proxy[0], proxy[1])}
    minimum = 200

    try:
        r = requests.get("http://zakupki.gov.ru", headers=headers, proxies= proxy)
        if (r.status_code == 200):
            print("{} работает. Время ответа {}".format(proxy, r.elapsed.microseconds/1000))
            if (r.elapsed.microseconds/1000 < minimum):
                best_proxy = [proxy,r.elapsed.microseconds]
            working_proxy.append(proxy)
    except Exception:
        print ("Прокси не работает {}")


print ("Количество прокси нашлось: {}".format (len(working_proxy)))
print ("Лучший прокси: {}".format (best_proxy))