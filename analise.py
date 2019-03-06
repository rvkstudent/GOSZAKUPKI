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

    result = ''

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

            if con:
                con.rollback()

        finally:
            if con:
                con.close()
    return result

def find_tenders_info(content, to_base, region):

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
            tender_link = ""

            tenderTds = tender.findAll("td", {"class": "tenderTd"})

            for tenderTd in tenderTds:

                dts = tenderTd.findAll("dt")
                auction_type = dts[0].get_text().strip(' \t\n')

                zakup = dts[1].get_text()

                #print(len(zakup.split()))

                if len(zakup.split()) > 3:
                    zakup_status = " ".join(zakup.split('/')[0].split())
                    #print(zakup_status)
                    zakup_zakon = zakup.split()[3]

                price_text = tenderTd.findAll("dd")[1].findAll("strong")
                if len(price_text) > 0:
                    price = "".join(price_text[0].get_text().split())


            descriptTenderTd = tender.find("td", {"class": "descriptTenderTd"})

            dts = descriptTenderTd.find("dt")

            tender_link = dts.find('a', href=True)['href']
            if 'http' not in tender_link:
                tender_link = 'http://zakupki.gov.ru{}'.format(tender_link)

            procedure_num = dts.get_text().split()[1]

            oraganisation = " ".join(
                descriptTenderTd.find(
                    "dd", {"class": "nameOrganization"})
                .get_text().split()).replace("Заказчик: ", "")

            description = " ".join(
                descriptTenderTd.findAll("dd")[1].get_text().split()).replace('\'', '\"')

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

            query = query + "INSERT INTO tenders_temp VALUES('{}','{}','{}',{},'{}','{}','{}', '{}',current_timestamp(0), '', '{}', '{}') ON CONFLICT DO NOTHING;".format(procedure_num, auction_type, zakup_status,
                                pg_price, pg_created, pg_modified, oraganisation, description, region, tender_link)


    print("Тендеров обработано: {}".format(len(tenders)))

    execute_query(query)



def find_tsc_tenders():



    execute_query("update tenders_temp set tsv = to_tsvector('ru',description);DROP INDEX textsearch_idx; create index textsearch_idx on tenders_temp using gin(tsv);" )

    execute_query(
        "update tenders_stat set last_update = current_timestamp(0), before = (select count(*) from tenders_tsc) where  change = 'update_tsc';")

    result = execute_query("insert into tenders_tsc (tender_id, auction_type, zakup_status, price, date_created, date_modified, organisation, description, date_found, phrase, region, tender_link) SELECT tenders_temp.tender_id, tenders_temp.auction_type, tenders_temp.zakup_status, tenders_temp.price, tenders_temp.date_created, tenders_temp.date_modified, tenders_temp.organisation, tenders_temp.description, tenders_temp.date_found, words.phrase, tenders_temp.region, tenders_temp.tender_link FROM tenders_temp, words  WHERE tenders_temp.tsv @@ plainto_tsquery('ru',words.phrase) ON CONFLICT(tender_id) DO NOTHING;")

    execute_query(
        "update tenders_stat set after = (select count(*) from tenders_tsc), last_update = current_timestamp(0) where change = 'update_tsc';")


    query = "insert into tenders(tender_id, auction_type, zakup_status, price, date_created, date_modified, organisation, description, date_found, region, tender_link) SELECT tenders_temp.tender_id, tenders_temp.auction_type, tenders_temp.zakup_status, tenders_temp.price, tenders_temp.date_created, tenders_temp.date_modified, tenders_temp.organisation, tenders_temp.description, tenders_temp.date_found, tenders_temp.region, tenders_temp.tender_link FROM tenders_temp ON CONFLICT DO NOTHING;DELETE FROM tenders_temp;"

    execute_query(query)

    execute_query("update tenders_tsc set tsv = to_tsvector('ru',description);DROP INDEX textsearch_idx; create index textsearch_idx on tenders_tsc using gin(tsv);")

    execute_query("DELETE FROM tenders_tsc WHERE tender_id in (SELECT tender_id FROM tenders_tsc, stop_words WHERE tenders_tsc.tsv @@ plainto_tsquery('ru',stop_words.s_word));")
