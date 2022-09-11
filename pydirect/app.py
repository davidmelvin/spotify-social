# from models import Result
from requests import request
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from accounts import save_followed_accounts_of_user

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///concert_buddies'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/', methods=["GET", "POST"])
def index():
    errors = []
    results = {}

    if request.method == "POST":
        try:
            user_id = request.form['url']
            # save_followed_accounts_of_user(user_id)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )

    return render_template('index.html', errors=errors, results=results)


@ app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()
