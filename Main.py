
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
import pandas as pd
import datetime
from pandas import ExcelWriter
import os


search_phrase = list()


f = open(os.path.join('/home/user/git_files/GOSZAKUPKI','phrase'))
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

#get_tender_report()

#ora_tender = pd.read_excel("c:\\GOSZAKUPKI\\ora_tender_{}".format(datetime.datetime.now().date()) +".xlsx")

zakupki_gov = pd.read_excel("home/user/GOSZAKUPKI/links_{}".format(datetime.datetime.now().date()) +".xls", dtype={ 'Номер процедуры':str, 'Дата размещения':datetime.date,'Дата обновления':datetime.date })

previous = pd.DataFrame()

directory = u'~/GOSZAKUPKI/PREVIOUS/'

for file in os.listdir(directory):
    if file.endswith(".xls"):

        previous  = pd.read_excel(directory + file, dtype={'Дата размещения':datetime.date,'Дата обновления':datetime.date })



print (previous.info())

previous = previous[["Номер процедуры", "№ зацепки", "Клиент по Ораклу", "Заказчик", "Потребность", "Начальная цена","Конкурс", "Статус", "Дата размещения", "Дата обновления", "Найдено по фразе", "Ссылка на тендер", "Исполнитель", "Примечания"]]
zakupki_gov = zakupki_gov[["Номер процедуры", "№ зацепки", "Клиент по Ораклу", "Заказчик", "Потребность", "Начальная цена","Конкурс", "Статус", "Дата размещения", "Дата обновления", "Найдено по фразе", "Ссылка на тендер", "Исполнитель", "Примечания"]]

compare = zakupki_gov.append(previous)

compare = compare.drop_duplicates("Ссылка на тендер", keep="last")

writer = ExcelWriter(u'home/user/GOSZAKUPKI/compare_{}.xls'.format(datetime.datetime.now().date()), datetime_format='dd.mm.yyyy', engine='xlsxwriter' )

compare.to_excel(writer, 'Итого', index=False)

workbook = writer.book
worksheet = writer.sheets['Итого']

cell_zalivka = workbook.add_format()
cell_zalivka.set_pattern(1)  # This is optional when using a solid fill.
cell_zalivka.set_bg_color('green')
cell_zalivka.set_align('center')
cell_zalivka.set_align('vcenter')
cell_zalivka.set_text_wrap()

cell_format_data = workbook.add_format()
cell_format_data.set_num_format('dd.mm.yyyy')
cell_format_data.set_align('center')
cell_format_data.set_align('vcenter')

cell_format_num = workbook.add_format()
cell_format_num.set_num_format('# ###')
cell_format_num.set_align('center')
cell_format_num.set_align('vcenter')

cell_format_header = workbook.add_format()
cell_format_header.set_bold()
cell_format_header.set_text_wrap()
cell_format_header.set_align('center')
cell_format_header.set_align('vcenter')

cell_format11 = workbook.add_format()

cell_format11.set_align('center')
cell_format11.set_align('vcenter')
cell_format11.set_text_wrap()

worksheet.set_column('A:A', 20)
worksheet.set_column('B:B', 15)
worksheet.set_column('C:C', 15)
worksheet.set_column('D:D', 40)
worksheet.set_column('E:E', 40)
worksheet.set_column('F:F', 15)
worksheet.set_column('G:G', 20)
worksheet.set_column('H:H', 20)
worksheet.set_column('I:I', 15)
worksheet.set_column('J:J', 15)
worksheet.set_column('K:K', 20)
worksheet.set_column('L:L', 20)
worksheet.set_column('M:M', 20)
worksheet.set_column('N:N', 20)


worksheet.write('A1', "Номер процедуры", cell_format_header)
worksheet.write_column('A2', compare["Номер процедуры"], cell_format11)
worksheet.write('B1', "№ зацепки", cell_format_header)
worksheet.write_column('B2', compare["№ зацепки"].fillna(''), cell_format11)
worksheet.write('C1', "Клиент по Ораклу", cell_format_header)
worksheet.write_column('C2', compare["Клиент по Ораклу"].fillna(''), cell_format11)
worksheet.write('D1', "Заказчик", cell_format_header)
worksheet.write_column('D2', compare["Заказчик"].fillna(''), cell_format11)
worksheet.write('E1', "Потребность", cell_format_header)
worksheet.write_column('E2', compare["Потребность"], cell_format11)
worksheet.write('F1', "Начальная цена", cell_format_header)
worksheet.write_column('F2', compare["Начальная цена"], cell_format_num)
worksheet.write('G1', "Конкурс", cell_format_header)
worksheet.write_column('G2', compare["Конкурс"].fillna(''), cell_format11)
worksheet.write('H1', "Статус", cell_format_header)
worksheet.write_column('H2', compare["Статус"].fillna(''), cell_format11)

date_format = workbook.add_format({'num_format': 'dd.mm.yyyy',
                                   'align': 'left'})

#compare["Дата обновления"] = compare["Дата обновления"].apply(lambda x: datetime.datetime.strptime(x, '%d.%m.%Y'))
#compare["Дата размещения"] = compare["Дата размещения"].apply(lambda x: datetime.datetime.strptime(x, '%d.%m.%Y'))

worksheet.write('I1', "Дата размещения", cell_format_header)
worksheet.write_column('I2', compare["Дата размещения"].fillna(''), date_format)
worksheet.write('J1', "Дата обновления", cell_format_header)
worksheet.write_column('J2', compare["Дата обновления"].fillna(''), date_format)

worksheet.write('K1', "Найдено по фразе", cell_format_header)
worksheet.write_column('K2', compare["Найдено по фразе"].fillna(''), cell_format11)

worksheet.write('L1', "Ссылка на тендер", cell_format_header)
worksheet.write_column('L2', compare["Ссылка на тендер"].fillna(''), cell_format11)

worksheet.write('M1', "Исполнитель", cell_format_header)
worksheet.write_column('M2', compare["Исполнитель"].fillna(''), cell_format11)

worksheet.write('N1', "Примечания", cell_format_header)
compare["Примечания"] = compare["Примечания"].fillna('')

i = 1
for primechanie in compare["Примечания"]:
    if "зацепка" in primechanie.lower():
        worksheet.write(i, 13, primechanie, cell_zalivka)
    else:
        worksheet.write(i, 13, primechanie, cell_format11)
    i+=1



writer.save()

#parse_page(driver, total_links)



