from requests import request
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from accounts import save_followed_accounts_of_user
from models import db


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

    if request.method == "POST":
        try:
            user_id = request.form['url']
            results = save_followed_accounts_of_user(user_id)
        except Exception as err:
            errors.append(
                err
            )

    return render_template('index.html', errors=errors, results=results)


@ app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()
