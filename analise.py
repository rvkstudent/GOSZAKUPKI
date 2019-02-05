#import psycopg2
import sys
import requests
from bs4 import BeautifulSoup


def find_tenders_info(content):

    soup = BeautifulSoup(content, 'html.parser')

    tenders = soup.findAll("div", {"class": "registerBox registerBoxBank margBtm20"})

    for tender in tenders:

        auction_type = ""
        zakup_status = ""
        zakup_zakon = ""
        price = 0
        procedure_num = ""
        razmesheno = ""
        oraganisation = ""
        obnovleno = ""

        tenderTds = tender.findAll("td", {"class": "tenderTd"})
        for tenderTd in tenderTds:

            dts = tenderTd.findAll("dt")
            auction_type = dts[0].get_text().strip(' \t\n')
            zakup_status = " ".join(dts[1].get_text().split('/')[0].split())
            zakup_zakon = dts[1].get_text().split()[3]
            price_text = tenderTd.findAll("dd")[1].findAll("strong")
            if len(price_text) > 0:
                price = "".join(price_text[0].get_text().split())


        descriptTenderTd = tender.findAll("td", {"class": "descriptTenderTd"})[0]

        dts = descriptTenderTd.findAll("dt")
        procedure_num  = dts[0].get_text().split()[1]

        oraganisation = " ".join(
            descriptTenderTd.findAll(
                "dd", {"class": "nameOrganization"})[0]\
            .get_text().split()).replace("Заказчик: ", "")

        description = " ".join(
            descriptTenderTd.findAll("dd")[1].get_text().split())

        amountTenderTds = tender.findAll("td", {"class": "amountTenderTd"})

        for amountTenderTd in amountTenderTds:
            lis = amountTenderTd.findAll("li")

            razmesheno = " ".join(lis[0].get_text()\
                                  .split()).replace("Размещено: ", "")
            obnovleno = " ".join(lis[1].get_text()\
                                 .split()).replace("Обновлено: ", "")
    #
    #     print ("Тип аукциона: {}".format(auction_type))
    #     print("Статус закупки: {}".format(zakup_status))
    #     print("Закон: {}".format(zakup_zakon))
    #     print("Начальная цена: {}".format(price))
    #     print("Номер процедуры: {}".format(procedure_num))
    #     print("Заказчик: {}".format(oraganisation))
    #     print("Размещено: {}".format(razmesheno))
    #     print("Обновлено: {}".format(obnovleno))
    #
        split_date = razmesheno.split('.')
        pg_created = "{}-{}-{}".\
            format(split_date[2], split_date[1], split_date[0])
        split_date = obnovleno.split('.')
        pg_modified = "{}-{}-{}".\
            format(split_date[2], split_date[1], split_date[0])

        if(isinstance(price,str)):
            pg_price = price.replace(',','.')
        else:
            pg_price = str(price)


    print("Тендеров нашлось: {}".format(len(tenders)))

    # con = None
    #
    # try:
    #     con = psycopg2.connect(
    #         host='localhost',
    #         dbname='goszakupki',
    #         user='postgres',
    #         password='sapromat')
    #
    #     cur = con.cursor()
    #     cur.execute("INSERT INTO tenders \
    #                 VALUES('{}','{}','{}',{},'{}','{}','{}', '{}') \
    #                 ON CONFLICT DO NOTHING;".format(
    #                 procedure_num, auction_type, zakup_status,
    #                 pg_price, pg_created, pg_modified, oraganisation,
    #                     description))
    #
    #     con.commit()
    #
    # except (psycopg2.DatabaseError):
    #     if con:
    #         con.rollback()
    #
    # finally:
    #     if con:
    #         con.close()


