from utils.requests import get_data_from_url

from models import Account, Follow
from models import db
from sqlalchemy.dialects.postgresql import insert


def get_all_accounts():
    try:
        accounts = Account.query.all()
    except Exception as err:
        raise Exception(f'Unable to read accounts: {err}')
    return accounts


def get_followed_accounts_of_user(user_id):
    url = "https://spclient.wg.spotify.com/user-profile-view/v3/profile/{params[user_id]}/following?market=from_token"

    params = {"user_id": user_id}

    print(f"getting followed accounts of {user_id}")

    data = get_data_from_url(url, params)

    return data.json()


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

                insert_account_if_not_exists = insert(Account).values(
                    **account.as_dict_without_id()).on_conflict_do_nothing()

                db.session.execute(insert_account_if_not_exists)

                db.session.commit()

                relationship = Follow(
                    follower_id=user_id,
                    following_id=source_id
                )

                insert_relationship_if_not_exists = insert(Follow).values(
                    **relationship.as_dict_without_id()).on_conflict_do_nothing()

                db.session.execute(insert_relationship_if_not_exists)
                db.session.commit()

        except Exception as err:
            raise Exception(
                f"Unable toadd account or follower to database. error: {err}")
    else:
        print(f"Didn't find any accounts user {user_id} follows!")
