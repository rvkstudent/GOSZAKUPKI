from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from Parse_page import parse_page
from Gather_links import gather_links

search_phrase = list()


f = open('phrase')
line = f.readline()
while line:
    search_phrase.append(line)
    line = f.readline()
f.close()


main_url = "http://zakupki.gov.ru"



params = urllib.parse.urlencode({'searchString': search_phrase, 'pageNumber': 1, 'morphology': 'on', 'openMode':'USE_DEFAULT_PARAMS','sortDirection': 'false', 'recordsPerPage': '_10' ,
                                 'showLotsInfoHidden': 'false', 'fz44':'on','fz223':'on', 'ppRf615':'on','af':'on','ca':'on',
                                 'pc':'on','pa':'on','currencyId': '-1','regionDeleted':'false','sortBy':'UPDATE_DATE', 'publishDateFrom':'01.01.2018'})

url = "http://zakupki.gov.ru/epz/order/extendedsearch/results.html?%s" % params

driver = webdriver.Firefox()

total_links = gather_links(driver, search_phrase)

print ("Собрано %s линков" % len(total_links))

parse_page(driver, total_links)

