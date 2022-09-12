from utils.requests import get_data_from_url

from models import Account
from models import db


def get_followed_accounts_of_user():
    try:
        accounts = Account.query.all()
    except Exception as err:
        raise Exception(f'Unable to read accounts: {err}')
    return accounts


def save_followed_accounts_of_user(user_id: str):
    followed_accounts = get_followed_accounts_of_user(user_id)

    if followed_accounts:
        try:
            accounts = followed_accounts["profiles"]

            for profile in accounts:
                uri = profile.get("uri", None)

                if not uri:
                    raise Exception(
                        "Unable to read uri for one of the profiles")

                name = profile.get("name", None)

                if not name:
                    raise Exception("Unable to read name for one of profiles")

                source_id = uri.split(":")[2]
                account_type = uri.split(":")[1]

                account = Account(
                    source_id=source_id,
                    name=name,
                    type=account_type
                )
                db.session.add(account)
                db.session.commit()

        except Exception as err:
            raise Exception(f"Unable to add item to database. error: {err}")
    else:
        print(f"Didn't find any accounts user {user_id} follows!")
