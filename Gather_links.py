from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from pandas import ExcelWriter
import pandas as pd

print (datetime.now().date().day)

to_date = datetime(datetime.now().date().year, datetime.now().date().month, datetime.now().date().day -7)

to_date = to_date.strftime('%d.%m.%Y')

main_url = "http://zakupki.gov.ru"

def make_url(page_number, search_phrase):

    params = urllib.parse.urlencode(
        {'searchString': search_phrase, 'pageNumber': page_number, 'morphology': 'on', 'openMode': 'USE_DEFAULT_PARAMS',
         'sortDirection': 'false', 'recordsPerPage': '_10',
         'showLotsInfoHidden': 'false', 'fz44': 'on', 'fz223': 'on', 'ppRf615': 'on', 'af': 'on', 'ca': 'on',
         'pc': 'on', 'pa': 'on', 'currencyId': '-1', 'regionDeleted': 'false', 'sortBy': 'UPDATE_DATE',
         'publishDateFrom': to_date})

    url = "http://zakupki.gov.ru/epz/order/extendedsearch/results.html?%s" % params

    return url

def gather_links (driver, search_phrases):

    links_total = []
    datalist = []

    for search_phrase in search_phrases:

        print ("{}Сбор линков по фразе {}".format(datetime.now(),search_phrase))

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

            j=1
            while j <= pages :
                url = make_url(j, search_phrase)
                driver.get(url)

                for urls in driver.find_elements_by_class_name("registerBox"):

                    tender_link = urls.find_element_by_partial_link_text('№').get_property('href')

                    raw_data = list()

                    dd_tags = urls.find_elements_by_tag_name("dd")
                    for each_dd in dd_tags:
                        raw_data.append(each_dd.text)
                    dt_tags = urls.find_elements_by_tag_name("dt")
                    for each_dt in dt_tags:
                        raw_data.append(each_dt.text)

                    data_tags = urls.find_elements_by_class_name("amountTenderTd")
                    for each_data in data_tags:
                        li_tags = each_data.find_elements_by_tag_name("li")
                        for each_li in li_tags:
                            raw_data.append(each_li.text)
                    i = 1

                    nach_cena = 0.0
                    zakazchik = ""
                    predmet = ""
                    konkurs = ""
                    status = ""
                    nomer = 0
                    razmesheno = ""
                    obnovleno = ""

                    for field in raw_data:

                        if ("Начальная цена" in field ):
                            nach_cena = int(field.split("Начальная цена")[1].split(",")[0].replace(" ","").strip(' \t\n\r'))
                        if ("Заказчик:" in field):
                            zakazchik = field.split("Заказчик:")[1].strip(' \t\n\r')
                        if (i == 5):
                            predmet = field
                        if (i == 6):
                            konkurs = field
                        if (i == 7):
                            status = field
                        if ("№ " in field):
                            nomer = field.split("№ ")[1]
                        if ("Размещено:" in field):
                            razmesheno = field.split("Размещено: ")[1].strip(' \t\n\r')
                        if ("Обновлено:" in field):
                            obnovleno = field.split("Обновлено: ")[1].strip(' \t\n\r')



                        i+=1

                    links_total.append([nomer,zakazchik,predmet ,nach_cena,  konkurs, status, razmesheno, obnovleno, search_phrase, tender_link ])


                #for urls in driver.find_elements_by_partial_link_text('№'):
                #    links_total.append([urls.get_property('href'), search_phrase, urls.text.split(" ")[1]])

                 #   print ("Найдена заявка " + urls.text)
                j+=1



    my_list = pd.DataFrame(links_total)

    my_list.columns = ["Номер процедуры","Заказчик","Потребность","Начальная цена", "Конкурс", "Статус", "Дата размещения", "Дата обновления", "Найдено по фразе", "Ссылка на тендер"]

    my_list["№ зацепки"] = ""
    my_list["Клиент по Ораклу"] = ""
    my_list["Исполнитель"] = ""
    my_list["Примечания"] = ""


    my_list = my_list[["Номер процедуры","№ зацепки","Клиент по Ораклу","Заказчик","Потребность","Начальная цена", "Конкурс", "Статус", "Дата размещения", "Дата обновления", "Найдено по фразе", "Ссылка на тендер", "Исполнитель", "Примечания"]]




    writer = ExcelWriter(u'home/user/GOSZAKUPKI/links_{}.xls'.format(datetime.now().date()), datetime_format='dd.mm.yyyy')

    my_list.to_excel(writer, 'Ссылки', index=False)

    writer.save()

    driver.close()

    return links_total
