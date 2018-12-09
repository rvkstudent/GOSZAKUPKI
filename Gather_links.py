from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

main_url = "http://zakupki.gov.ru"

def make_url(page_number, search_phrase):
    params = urllib.parse.urlencode(
        {'searchString': search_phrase, 'pageNumber': page_number, 'sortDirection': 'false', 'recordsPerPage': '_10',
         'showLotsInfoHidden': 'false', 'fz44': 'on', 'fz223': 'on', 'ppRf615': 'on', 'af': 'on', 'ca': 'on',
         'pc': 'on', 'pa': 'on', 'currencyId': '-1', 'regionDeleted': 'false', 'sortBy': 'UPDATE_DATE'})

    url = "http://zakupki.gov.ru/epz/order/quicksearch/search_eis.html?%s" % params

    return url

def gather_links (driver, search_phrases):


    for search_phrase in search_phrases:

        url = make_url(1, search_phrase)

        driver.get(url)

        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'allRecords')))

        finally:
            print('No exception')

        pages = int(driver.find_element_by_class_name('allRecords').text.split(": ")[1]) % 10
        links_total = []
        i=1
        while i <= pages :
            url = make_url(i, search_phrase)
            driver.get(url)
            for urls in driver.find_elements_by_partial_link_text('№'):
                links_total.append(urls.get_property('href'))
            i+=1

    return links_total


    driver.close()
