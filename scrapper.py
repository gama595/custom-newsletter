import sqlite3

import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import log
logger = log.setup_custom_logger()


class Scrapper():

    def __init__(self):
        self.stringParams = []
        self.start_urls = []
        self.prod_name = []
        self.prod_price = []

        self.con = sqlite3.connect("myDadaBase.db", check_same_thread=False)
        self.cur = self.con.cursor()

    def build_urls(self, stringParams):
        for string in stringParams:
            string = string.replace(" ", "+")
            self.start_urls.append(
                "https://www.amazon.com.br/s?k="+str(string))
        return (self.start_urls)

    def get_url_params(self):
        res = self.cur.execute("SELECT product FROM requests")
        for resp in res.fetchall():
            self.stringParams.append(resp[0])
        return(self.stringParams)

    def crawler(self, urls):
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)

        for url in urls:
            driver.get(url)
            time.sleep(2.5)
            name = driver.find_element(
                By.CSS_SELECTOR, '.widgetId\=search-results_1 .a-color-base.a-text-normal').text
            price = driver.find_element(
                By.CSS_SELECTOR, '.widgetId\=search-results_1 .a-price-whole').text
            price_fraction = driver.find_element(
                By.CSS_SELECTOR, '.widgetId\=search-results_1 .a-price-fraction').text
            self.prod_name.append(name)
            self.prod_price.append(price+','+price_fraction)
            logger.info(f'Produto: {name} adicionado a lista')

        logger.info(
            f'{len(self.prod_name)} produtos encontrados pelo crawler\n')

    def save_data(self, urlParams):
        name_list = urlParams
        list_prods = []

        for i in range(0, len(self.prod_price)):
            list_prods.append(
                (name_list[i], self.prod_name[i], self.prod_price[i]))

        for item in list_prods:
            res = self.cur.execute(
                "SELECT prodid FROM products WHERE marketname = ?", (item[1:2][0], ))
            currId = res.fetchone()

            if currId is None:
                res = self.cur.execute(
                    "SELECT user FROM requests WHERE product = ?", (item[0:1][0], ))
                currUser = res.fetchone()
                self.cur.execute("INSERT INTO products(prodname, marketname, price, user) VALUES(?, ?, ?, ?)", (
                    item[0:1][0], item[1:2][0], item[2:3][0], str(currUser[0:1][0]), ))
                self.con.commit()
                logger.info(
                    f'Produto {item[1:2][0]} inserido com sucesso no banco')
            else:
                self.cur.execute(
                    "UPDATE products SET price = ? WHERE prodid = ?", (item[2:3][0], currId[0:1][0], ))
                self.con.commit()
                logger.info(
                    f'Produto {item[1:2][0]} atualizado com sucesso no banco')

    def execute_crawler():
        logger.info(f'--- Inicio da execução do crawler ---')
        myScrapper = Scrapper()
        myUrlsParams = myScrapper.get_url_params()
        myUrls = myScrapper.build_urls(myUrlsParams)
        myScrapper.crawler(myUrls)
        myScrapper.save_data(myUrlsParams)
        logger.info('--- Fim da execução do crawler ---')
