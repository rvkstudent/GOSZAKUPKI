import requests
import pickle


headers = {"Host": "zakupki.gov.ru",
           "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
           "Accept-Encoding": "gzip, deflate",
           "Referer": "http://zakupki.gov.ru/epz/main/public/home.html",
           "Connection": "keep-alive",
           "Cookie": "routeepz7=1; routeepz0=3; routeepz2=0; _ym_uid=154858942172065130; _ym_d=1548589421; _ym_isad=2",
           "Upgrade-Insecure-Requests": "1",
           "Cache-Control": "max-age=0"}

def connection_proxy():

    connection_proxy = {}
    last_proxy = {}

    with open('last_proxy', 'rb') as inp:
       last_proxy = pickle.load(inp)



    # пробуем с последним прокси из файла

    if (len(last_proxy) > 0):

            #last_proxy = {'http': 'http://109.173.73.116:8080/'}

            try:
                r = requests.get(
                    'http://zakupki.gov.ru/epz/order/quicksearch/search.html#',
                    headers=last_proxy[1], proxies=last_proxy[0])
                if (r.status_code == 200):
                    connection_proxy = last_proxy[0]
            except requests.RequestException:
                print("Exception")

    # если доступных прокси не нашлось - запускаем проверку всех вариантов

    if (len(connection_proxy) == 0):

        with open('proxy_list', 'rb') as inp:
            working_proxy = pickle.load(inp)

        proxies = [{'http': 'http://kozlov.r:Fvcnthlfv2019@10.77.20.61:3128/'}, {'http': ''}]

        proxies.extend(working_proxy)

        minimum = 200
        best_proxy = ''

        for proxy in proxies:

            print(proxy)

            try:
                r = requests.get(
                    'http://zakupki.gov.ru/epz/order/quicksearch/search.html#',
                    headers=headers, proxies=proxy)
                if (r.status_code == 200):
                    connection_speed = r.elapsed.microseconds / 1000
                    connection_proxy = proxy
                    if (connection_speed < minimum):
                        best_proxy = proxy
                        minimum = connection_speed

            except requests.RequestException:
                print ("Exception")


        if (len(best_proxy) > 0 ):
            connection_proxy = best_proxy

        with open('last_proxy', 'wb') as out:
            pickle.dump([connection_proxy, headers], out)

    return connection_proxy, headers

if __name__ == "__main__":

    proxy = connection_proxy()
    print ("Величина словаря: {}".format(len(proxy)))
    if (len(proxy) > 0):
        print("Выбран прокси: {}".format(proxy))
        r = requests.get(
            'http://zakupki.gov.ru/', headers=headers, proxies=proxy[0])
        print ("Статус соединения: {}".format(r.status_code))
