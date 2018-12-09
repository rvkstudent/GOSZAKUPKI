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

search_phrase = ["ремонт Хитачи"]
main_url = "http://zakupki.gov.ru"

params = urllib.parse.urlencode({'searchString': search_phrase, 'pageNumber': 1, 'sortDirection': 'false', 'recordsPerPage': '_10' ,
                                 'showLotsInfoHidden': 'false', 'fz44':'on','fz223':'on', 'ppRf615':'on','af':'on','ca':'on',
                                 'pc':'on','pa':'on','currencyId': '-1','regionDeleted':'false','sortBy':'UPDATE_DATE'})

url = "http://zakupki.gov.ru/epz/order/quicksearch/search_eis.html?%s" % params

driver = webdriver.Firefox()

#total_links = gather_links(driver, search_phrase)


parse_page(driver, ['http://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?regNumber=31807023032'])

