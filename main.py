from crawler import Crawler
from sender import EmailSender
from datetime import datetime
import sqlite3

import log
logger = log.setup_custom_logger()

class Main():

    def load_database():
        # Conectando com o banco
        con = sqlite3.connect("myDadaBase.db", check_same_thread=False)
        cur = con.cursor()

        # Estabelecendo as tabelas
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

    try:
        load_database()
    except Exception as e:
        logger.error(f'Falha ao carregar a base de dados: {e}')

    def execute_crawler():
        logger.info(f'Crawler executado : {datetime.now()}\n')
        Crawler.execute_crawler()

    def send_message(period):
        logger.info(f'Email sender executado : {datetime.now()}\n')
        EmailSender.sender(period)

# Linhas de comando manuais
# python -c "from main import *; Main.execute_crawler()"
# python -c "from main import *; Main.send_message(1)"
# python -c "from main import *; Main.send_message(2)"
# python main.py
