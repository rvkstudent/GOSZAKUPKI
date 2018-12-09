from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from lxml import html


main_url = "http://zakupki.gov.ru"

def parse_page (driver, links):

    driver.execute_script("window.open('');")
    tabs = driver.window_handles
    driver.switch_to.window(tabs[1])

    for link in links:


        driver.get(link)

        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'td')))

        finally:
            print('No exception')

        elements = driver.find_elements_by_tag_name('td')

        for el in elements:

            ###### получаем URL ПРОТОКОЛА

            if ('ПРОТОКОЛ' in el.text):
                el.click()

                try:
                    wait = WebDriverWait(driver, 10)
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'toolTipMenu')))

                finally:
                    print('No exception')

                hover_link = driver.find_elements_by_class_name('toolTipMenu')[0]
                hover = ActionChains(driver).move_to_element(hover_link)
                hover.perform()
                elements = driver.find_elements_by_tag_name('li')

                for el in elements:

                    if ('Печат' in el.text):
                        a = el.get_attribute('onclick')
                        url_prorocol = "{}{}".format(main_url, a.split("\'")[1])
                        print(url_prorocol)

                break

            ###### Получаем Общие сведения о закупке

        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'td')))
        finally:
            print('No exception')

        td_menu = driver.find_elements_by_tag_name('td')

        for tds in td_menu:



            if ('ОБЩАЯ' in tds.text):
                tds.click()

                try:
                    wait = WebDriverWait(driver, 10)
                    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'td')))

                finally:
                    print('No exception')

                td_inside = driver.find_elements_by_tag_name('td')

                previous_element = ''

                for tds_in in td_inside:

                    if ('ИНН' in previous_element):
                        print('ИНН:' + tds_in.text)
                    if ('Наименование организации' in previous_element):
                        print('Наименование организации:' + tds_in.text)
                    if ('Дата размещения текущей редакции извещения' in previous_element):
                        print('Дата размещения текущей редакции извещения:' + tds_in.text)
                    if ('Наименование закупки' in previous_element):
                        print('Наименование закупки:' + tds_in.text)


                    previous_element = tds_in.text
                break

        ###### Получаем ДОКУМЕНТЫ

        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'td')))
        finally:
            print('No exception')

        td_menu = driver.find_elements_by_tag_name('td')

        for tds in td_menu:

            if ('ДОКУМЕНТЫ' in tds.text):
                tds.click()

                try:
                    wait = WebDriverWait(driver, 10)
                    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'td')))

                finally:
                    print('No exception')

                elem = driver.find_element_by_xpath("//a[@class='epz_aware']")

                print (elem.text)
                print(elem.get_property('href'))


                break

    driver.close()
