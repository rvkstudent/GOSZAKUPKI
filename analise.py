# -*- coding: utf-8 -*-
import psycopg2
import sys
import requests
from bs4 import BeautifulSoup
import time


class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print("Elapsed time: {:.3f} sec".format(time.time() - self._startTime))


def execute_query(query):
    with Profiler() as p:

        con = None

        try:
            con = psycopg2.connect(
                host='localhost',
                dbname='goszakupki',
                user='postgres',
                password='sapromat')

            cur = con.cursor()

            cur.execute(query)

            con.commit()


        except psycopg2.DatabaseError as error:

            print(error)
            print(query)

            if con:
                con.rollback()

        finally:
            if con:
                con.close()


def find_tenders_info(content, to_base):

    soup = BeautifulSoup(content, 'html.parser')

    tenders = soup.findAll("div", {"class": "registerBox registerBoxBank margBtm20"})

    query = ''


    with Profiler() as p:
        for tender in tenders:

            auction_type = ""
            zakup_status = ""
            zakup_zakon = ""
            price = 0
            procedure_num = ''
            razmesheno = ""
            oraganisation = ""
            obnovleno = ""

            tenderTds = tender.findAll("td", {"class": "tenderTd"})

            for tenderTd in tenderTds:

                dts = tenderTd.findAll("dt")
                auction_type = dts[0].get_text().strip(' \t\n')

                zakup = dts[1].get_text()

                if len(zakup.split()) == 3:
                    zakup_status = " ".join(zakup.split('/')[0].split())
                    zakup_zakon = zakup.split()[3]

                price_text = tenderTd.findAll("dd")[1].findAll("strong")
                if len(price_text) > 0:
                    price = "".join(price_text[0].get_text().split())


            descriptTenderTd = tender.find("td", {"class": "descriptTenderTd"})

            dts = descriptTenderTd.find("dt")
            procedure_num = dts.get_text().split()[1]

            oraganisation = " ".join(
                descriptTenderTd.find(
                    "dd", {"class": "nameOrganization"})
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

            # print ("Тип аукциона: {}".format(auction_type))
            # print("Статус закупки: {}".format(zakup_status))
            # print("Закон: {}".format(zakup_zakon))
            # print("Начальная цена: {}".format(price))
            # print("Номер процедуры: {}".format(procedure_num))
            # print("Заказчик: {}".format(oraganisation))
            # print("Размещено: {}".format(razmesheno))
            # print("Обновлено: {}".format(obnovleno))

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

            query = query + "INSERT INTO tenders_temp VALUES('{}','{}','{}',{},'{}','{}','{}', '{}',current_timestamp(0)) ON CONFLICT DO NOTHING;".format(procedure_num, auction_type, zakup_status,
                                pg_price, pg_created, pg_modified, oraganisation, description)


    print("Тендеров обработано: {}".format(len(tenders)))

    execute_query(query)



def find_tsc_tenders():

    query = "update tenders_temp set tsv = to_tsvector('ru',description);create index on tenders_temp using gin(tsv);insert into tenders_tsc SELECT tenders_temp.tender_id, tenders_temp.auction_type, tenders_temp.zakup_status, tenders_temp.price, tenders_temp.date_created, tenders_temp.date_modified, tenders_temp.organisation, tenders_temp.description, tenders_temp.date_found, words.phrase FROM tenders_temp, words  WHERE tenders_temp.tsv @@ plainto_tsquery('ru',words.phrase) ON CONFLICT DO NOTHING;"

    query = query + "insert into tenders SELECT tenders_temp.tender_id, tenders_temp.auction_type, tenders_temp.zakup_status, tenders_temp.price, tenders_temp.date_created, tenders_temp.date_modified, tenders_temp.organisation, tenders_temp.description, tenders_temp.date_found FROM tenders_temp ON CONFLICT DO NOTHING;DELETE FROM tenders_temp;"

    execute_query(query)