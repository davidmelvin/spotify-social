from utils.requests import get_data_from_url

from models import Account
from models import db


def get_followed_accounts_of_user(user_id: str):
    url = "https://spclient.wg.spotify.com/user-profile-view/v3/profile/{params[user_id]}/following?market=from_token"

    params = {"user_id": user_id}

    print(f"getting followed accounts of {user_id}")

    return get_data_from_url(url, params)


def save_followed_accounts_of_user(user_id: str):
    followed_accounts = get_followed_accounts_of_user(user_id)

    if followed_accounts:
        try:
            accounts = followed_accounts["profiles"]

            for profile in accounts:
                uri = profile.get("uri", "unkown uri")

                if ":user:" in uri:
                    type = "user"
                else:
                    type = "artist"

                account = Account(
                    uri=uri,
                    name=profile.get("name", "unknown name"),
                    type=type
                )
                db.session.add(account)
                db.session.commit()

        except Exception as err:
            raise Exception(f"Unable to add item to database. error: {err}")
    else:
        print(f"Didn't find any accounts user {user_id} follows!")
