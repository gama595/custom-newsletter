import smtplib
import ssl
from email.message import EmailMessage
import sqlite3

import log
logger = log.setup_custom_logger()


class EmailSender():
    def __init__(self, receiverEmail, message, subject):
        self.receiverEmail = receiverEmail
        self.message = message
        self.subject = subject

        self.port = 465  # SSL
        self.smtp_server = "smtp.gmail.com"  # gmail service

        self.con = sqlite3.connect("myDadaBase.db", check_same_thread=False)
        self.cur = self.con.cursor()

        secrets = []
        with open('senderemail.txt') as f:
            secrets = (f.readlines())
            secrets = [s.replace('\n', '') for s in secrets]
        self.sender_email = secrets[0].replace('email: ', '')
        self.password = secrets[1].replace('password: ', '')

    def say_hello(self):
        print('receiver: '+self.receiverEmail)
        print('message: '+self.message)
        print('subject: '+self.subject)
        logger.info(
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

    # def sender(receiverEmail, message, subject):
    #     sender = EmailSender(receiverEmail, message, subject)
    #     sender.say_hello()
    #     # sender.send_email()
    #     logger.info(f'--- Menssagem enviada para {receiverEmail} ---')
