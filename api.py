from flask import Flask, request
from email_validator import validate_email, EmailNotValidError
import sqlite3

con = sqlite3.connect("myDadaBase.db", check_same_thread=False)
cur = con.cursor()


def register_user(name, email):
    cur.execute("INSERT INTO users(name, email) VALUES (?, ?)", (name, email))
    con.commit()


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
    cur.execute("INSERT INTO requests(product, period, user) VALUES (?, ?, ?)",
                (product, period, user))
    con.commit()


app = Flask(__name__)


@app.route("/register", methods=["POST"])
def get_data():

    json_data = request.json
    name = json_data['name']
    email = json_data['email']
    status = True

    if validade_name(name) == False:
        status = False
    if validade_email(email) == False:
        status = False

    if status == True:
        register_user(name, email)
        return {"Message: ": "User registration success"}
    else:
        return {"Message: ": "User registration failed"}


@app.route("/register-request", methods=["POST"])
def set_user_prefs():

    json_data = request.json

    product = json_data['product']
    period = json_data['period']
    email = json_data['user-email']
    status = True

    # if validade_product(product) == False: status = False
    if validade_email_exist(email) == False:
        status = False
    if validade_period(period) == False:
        status = False

    if status == True:
        register_request(product, period, email)
        return {"Message: ": "Request registration success"}
    else:
        return {"Message: ": "Request registration failed"}


# Iniciando API
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5051)
