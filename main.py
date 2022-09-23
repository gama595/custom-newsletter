from crawler import Crawler
from sender import EmailSender
from datetime import datetime
import sqlite3
import time

import log
logger = log.setup_custom_logger()


class Main():

    def say_hello():
        print('hello')

    def load_database():
        con = sqlite3.connect("myDadaBase.db", check_same_thread=False)
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS users(
        userid INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE)""")
        con.commit()

        cur. execute("""CREATE TABLE IF NOT EXISTS requests(
        reqid INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT NOT NULL,
        period INTERGER NOT NULL,
        user TEXT NOT NULL,
        FOREIGN KEY(user) REFERENCES users(email))""")
        con.commit()

        cur.execute("""CREATE TABLE IF NOT EXISTS products(
                            prodid INTEGER PRIMARY KEY AUTOINCREMENT,
                            prodname TEXT NOT NULL,
                            marketname TEXT NOT NULL UNIQUE,
                            price TEXT NOT NULL,
                            user TEXT NOT NULL,
                            FOREIGN KEY(user) REFERENCES users(email))""")
        con.commit()
        logger.info(f'Database carregado : {datetime.now()}\n')

    load_database()

    def say_hi(msg):
        print(msg)

    def execute_crawler():
        logger.info(f'Crawler executado : {datetime.now()}\n')
        Crawler.execute_crawler()

    def send_message(period):
        logger.info(f'Email sender executado : {datetime.now()}\n')
        con = sqlite3.connect("myDadaBase.db", check_same_thread=False)
        cur = con.cursor()

        res = cur.execute(
            "SELECT user FROM requests WHERE period = ?", (period, ))
        emails = res.fetchall()
        email_list = []
        msg = ''

        for email in emails:
            email_list.append(email)
            email_list = list(dict.fromkeys(email_list))

        for email in email_list:
            msg = ''
            res = cur.execute(
                "SELECT marketname price FROM products WHERE user = ?", (email[0:1][0], ))
            products = res.fetchall()
            res = cur.execute(
                "SELECT price FROM products WHERE user = ?", (email[0:1][0], ))
            price = res.fetchall()

            res = cur.execute(
                "SELECT name FROM users WHERE email = ?", (email[0:1][0], ))
            userName = res.fetchall()
            for i in range(0, len(products)):
                msg += f'Produto: {products[(i):(i+1)][0][0]}\nPreço: R$ {price[(i):(i+1)][0][0]}\n\n'
            subj = f"Olá {userName[0:1][0][0]} aqui estão os dados de sua inscrição"
            my_sender = EmailSender(str(email[0:1][0]), str(msg), str(subj))
            # my_sender.say_hello()
            my_sender.send_email()
            time.sleep(2.5)

    # from datetime import datetime

    # file = open('file.txt', 'a')

    # file.write(f'{datetime.now()} - The scipt ran \n')


# python -c "from main import *; Main.execute_crawler()"
# python -c "from main import *; Main.send_message(1)"
# python -c "from main import *; Main.send_message(2)"
# python main.py
