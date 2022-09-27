from requests import request
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import accounts
from models import db
import logging
# from logging.config import dictConfig
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger("concert_buddies")
logger.setLevel(logging.DEBUG)
# logger.debug("PLSSSS")


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///concert_buddies'

    db.init_app(app)

    migrate = Migrate(app, db)

    return app


app = create_app()


@app.route('/', methods=["GET", "POST"])
def index():
    errors = []
    results = {}

    if request.method == "GET":
        try:
            results = accounts.get_all_accounts()
        except Exception as err:
            errors.append(err)

    if request.method == "POST":
        try:
            user_id = request.form['url']
            results = accounts.save_followed_accounts_of_user(
                user_id=user_id, recur=True)
        except Exception as err:
            errors.append(
                err
            )

    return render_template('index.html', errors=errors, results=results)


@app.route("/mutuals/", methods=["POST"])
def mutuals():
    errors = []
    results = {}

    if request.method == "POST":
        try:
            user_id = request.form['url']
            # results = accounts.
            results = []

        except Exception as err:
            errors.append(
                err
            )

        return render_template('mutuals.html', errors=errors, results=results)


@ app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()
