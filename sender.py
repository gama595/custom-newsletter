import smtplib
import ssl
from email.message import EmailMessage
import sqlite3

import log
import time
logger = log.setup_custom_logger()


class EmailSender():
    def __init__(self, receiverEmail, message, subject):
        self.receiverEmail = receiverEmail
        self.message = message
        self.subject = subject

        self.port = 465  # SSL
        self.smtp_server = "smtp.gmail.com"  # gmail service

        # Conectando com o banco
        try:
            self.con = sqlite3.connect(
                "myDadaBase.db", check_same_thread=False)
            self.cur = self.con.cursor()
        except Exception as e:
            logger.error(f'Crawler - Erro ao conectar ao banco: {e}')

        # Lendo arquivo de usuario e senha
        try:
            secrets = []
            with open('senderemail.txt') as f:
                secrets = (f.readlines())
                secrets = [s.replace('\n', '') for s in secrets]
            self.sender_email = secrets[0].replace('email: ', '')
            self.password = secrets[1].replace('password: ', '')
        except Exception as e:
            logger.error(f'Sender - Erro ao ler arquivo senderemail.txt: {e}')

    # Metodo para testar o email
    def say_hello(self):
        print('receiver: '+self.receiverEmail)
        print('message: '+self.message)
        print('subject: '+self.subject)
        logger.debug(
            f'--- Menssagem teste enviada para {self.receiverEmail} ---')

    def set_receiver_email(self, receiverEmail):
        self.receiverEmail = receiverEmail

    def set_message(self, message):
        self.message = message

    def set_subject(self, subject):
        self.subject = subject

    def send_email(self):
        msg = EmailMessage()
        msg.set_content(self.message)

        msg['From'] = self.sender_email
        msg['To'] = self.receiverEmail
        msg['Subject'] = self.subject

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.send_message(msg)

        logger.info(f'--- Menssagem enviada para {self.receiverEmail} ---')

    def sender(self, period):

        # Recolhendo emails de usuarios no ciclo semanal/mensal
        try:
            res = self.cur.execute(
                "SELECT user FROM requests WHERE period = ?", (period, ))
            emails = res.fetchall()
            email_list = []
            msg = ''
        except Exception as e:
            logger.error(f'Sender - Erro ao encontrar requisições: {e}')

        try:
            # criando uma lista de emails
            for email in emails:
                email_list.append(email)
                email_list = list(dict.fromkeys(email_list))

            # Recuperando dados dos produtos relacionados ao usuario e então criando o corpo da mensagem que sera enviado por email
            for email in email_list:
                msg = ''
                res = self.cur.execute(
                    "SELECT marketname price FROM products WHERE user = ?", (email[0:1][0], ))
                products = res.fetchall()
                res = self.cur.execute(
                    "SELECT price FROM products WHERE user = ?", (email[0:1][0], ))
                price = res.fetchall()

                res = self.cur.execute(
                    "SELECT name FROM users WHERE email = ?", (email[0:1][0], ))
                userName = res.fetchall()
                for i in range(0, len(products)):
                    msg += f'Produto: {products[(i):(i+1)][0][0]}\nPreço: R$ {price[(i):(i+1)][0][0]}\n\n'
                subj = f"Olá {userName[0:1][0][0]} aqui estão os dados de sua inscrição"
                my_sender = EmailSender(
                    str(email[0:1][0]), str(msg), str(subj))

                # Para nao enviar emails, troque essa linha comentada com a de baixo e o conteudo do email aparecera no console
                # my_sender.say_hello()
                my_sender.send_email()

                time.sleep(2.5)

        except Exception as e:
            logger.error(f'Sender - Erro ao enviar email: {e}')
