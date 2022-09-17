from utils.requests import get_data_from_url

from models import Account, Follow
from models import db
from sqlalchemy.dialects.postgresql import insert
# from app import app

import logging

logger = logging.getLogger("concert_buddies")


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
    try:
        data = get_data_from_url(url, params)
        if not data:
            logger.info(
                "got error trying to get followed accounts of user: %s", user_id)
            return None
        # print(data.json())

        # logger.info("get_followed_accounts_of_user:\n %s", data)

        return data.json()
    except Exception as err:
        error = f"failed to return get_followed_accounts_of_user as JSON: {err}"
        logger.error(error)
        raise Exception(error)

    # return data.json()


def save_followed_accounts_of_user(user_id: str, recur: bool = None):
    followed_accounts = get_followed_accounts_of_user(user_id)

    if followed_accounts:
        try:
            accounts = followed_accounts["profiles"]
            print(f"{user_id} follows {len(accounts)} accounts. saving them!")

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

                try:
                    account = Account(
                        source_id=source_id,
                        name=name,
                        type=account_type
                    )

                    insert_account_if_not_exists = insert(Account).values(
                        **account.as_dict_without_id()).on_conflict_do_nothing()

                    db.session.execute(insert_account_if_not_exists)

                    db.session.commit()
                except Exception as err:
                    error = f"Unable to add account to database. error: {err}"
                    logger.error(error)
                    raise Exception(error)

                try:
                    relationship = Follow(
                        follower_id=user_id,
                        following_id=source_id
                    )

                    insert_relationship_if_not_exists = insert(Follow).values(
                        **relationship.as_dict_without_id()).on_conflict_do_nothing()

                    db.session.execute(insert_relationship_if_not_exists)
                    db.session.commit()
                except Exception as err:
                    error = f"Unable to add follower relationship to database. error: {err}"
                    logger.error(error)
                    raise Exception(error)

                if account_type == "user" and recur:
                    save_followed_accounts_of_user(
                        user_id=source_id, recur=None)

        except Exception as err:
            error = f"Unable to add account or follower to database. error: {err}"
            logger.error(error)
            raise Exception(error)
    else:
        print(f"Didn't find any accounts user {user_id} follows!")


# def get_accounts_followed_by_friends_of_user(user_id: str):
#     friends = db.query(Follow).filter_by(follower_id=user_id).all()

#     print(friends)
