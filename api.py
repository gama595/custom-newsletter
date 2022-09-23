from flask import Flask, request
from email_validator import validate_email, EmailNotValidError
import sqlite3
from flask.logging import default_handler as handler
from datetime import datetime

import log
logger = log.setup_custom_logger()
logger.getLogger('werkzeug').disabled = True

try:
    con = sqlite3.connect("myDadaBase.db", check_same_thread=False)
    cur = con.cursor()
except Exception as e:
    logger.error(f'API - Erro ao conectar ao banco: {e}')


def register_user(name, email):
    try:
        cur.execute("INSERT INTO users(name, email) VALUES (?, ?)",
                    (name, email))
        con.commit()
        logger.info(f'API - Usuario inserido ao banco: {name}')
        return True
    except Exception as e:
        logger.error(f'API - Erro ao conectar ao banco: {e}')
        return False


def validade_name(name):
    if name.replace(" ", "").isalpha() and all([x == True for x in [*map(lambda x: True if len(x) >= 3 else False, name.split())]]):
        return True
    else:
        return False


def validade_email(email):
    try:
        validate_email(email).email
        return True
    except EmailNotValidError as e:
        return False


def validade_period(period):
    if period >= 0 and period < 3:
        return True
    else:
        return False


def validade_email_exist(email):
    res = cur.execute(
        "SELECT name, email FROM users WHERE email = ?", (email, ))
    if res.fetchone():
        return True
    else:
        return False


def register_request(product, period, user):
    try:
        cur.execute("INSERT INTO requests(product, period, user) VALUES (?, ?, ?)",
                    (product, period, user))
        con.commit()
        logger.info(f'API - Request inserido ao banco: {product}')
        return True
    except Exception as e:
        logger.error(f'API - Erro ao conectar ao banco: {e}')
        return False


app = Flask(__name__)
app.logger.removeHandler(handler)


@app.route("/register", methods=["POST"])
def get_data():

    try:
        json_data = request.json
        name = json_data['name']
        email = json_data['email']
        status = True
    except Exception as e:
        logger.error(f'API - Erro ao ler dados da api: {e}')

    if validade_name(name) == False:
        logger.warning(f'API - Tentativa de cadastro, nome invalido')
        status = False
    if validade_email(email) == False:
        status = False
        logger.warning(f'API - Tentativa de cadastro, email invalido')

    if status == True:
        if register_user(name, email) == True:
            return {"Message: ": "User registration success"}
        else:
            return {"Message: ": "User registration failed"}
    else:
        return {"Message: ": "User registration failed"}


@app.route("/register-request", methods=["POST"])
def set_user_prefs():

    try:
        json_data = request.json

        product = json_data['product']
        period = json_data['period']
        email = json_data['user-email']
        status = True
    except Exception as e:
        logger.error(f'API - Erro ao ler dados da api: {e}')

    if validade_email_exist(email) == False:
        status = False
        logger.warning(f'API - Tentativa de cadastro, email não existente')
    if validade_period(period) == False:
        status = False
        logger.warning(f'API - Tentativa de cadastro, periodo invalido')

    if status == True:
        if register_request(product, period, email) == True:
            return {"Message: ": "Request registration success"}
        else:
            return {"Message: ": "Request registration failed"}
    else:
        return {"Message: ": "Request registration failed"}

    # Iniciando API
if __name__ == "__main__":
    try:
        logger.info(f'API executada : {datetime.now()}\n')
        app.run(host='0.0.0.0', port=5051)
    except Exception as e:
        logger.error(f'API - Erro iniciar api: {e}')
