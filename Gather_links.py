from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException

main_url = "http://zakupki.gov.ru"

def make_url(page_number, search_phrase):

    params = urllib.parse.urlencode(
        {'searchString': search_phrase, 'pageNumber': page_number, 'morphology': 'on', 'openMode': 'USE_DEFAULT_PARAMS',
         'sortDirection': 'false', 'recordsPerPage': '_10',
         'showLotsInfoHidden': 'false', 'fz44': 'on', 'fz223': 'on', 'ppRf615': 'on', 'af': 'on', 'ca': 'on',
         'pc': 'on', 'pa': 'on', 'currencyId': '-1', 'regionDeleted': 'false', 'sortBy': 'UPDATE_DATE',
         'publishDateFrom': '01.01.2018'})

    url = "http://zakupki.gov.ru/epz/order/extendedsearch/results.html?%s" % params

    return url

def gather_links (driver, search_phrases):

    links_total = []

    for search_phrase in search_phrases:

        url = make_url(1, search_phrase)

        driver.get(url)

        has_protocols = True

        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'allRecords')))
        except TimeoutException:
            has_protocols = False
        finally:
            print('No exception')
        if (has_protocols == True):
            links_found = int(driver.find_element_by_class_name('allRecords').text.split(": ")[1])
            pages = links_found // 10
            if links_found > 0 and pages == 0:
                pages = 1

            i=1
            while i <= pages :
                url = make_url(i, search_phrase)
                driver.get(url)
                for urls in driver.find_elements_by_partial_link_text('№'):
                    links_total.append(urls.get_property('href'))
                    print ("Найдена заявка " + urls.text)
                i+=1

    return links_total


    driver.close()
