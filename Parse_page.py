from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

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

        elements = driver.find_elements_by_tag_name('td')

        for el in elements:

            if ('ОБЩАЯ' in el.text):
                el.click()

            try:
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'noticeBoxH2')))

            finally:
                print('No exception')

            elements = driver.find_elements_by_tag_name('td')

            previous_element = ''

            for el in elements:

                if ('ИНН' in previous_element):
                    print('ИНН:' + el.text)
            previous_element = el.text


    driver.close()
