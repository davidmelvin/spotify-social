from urllib.error import HTTPError

from credentials import api_access_token
from utils.requests import get_data_from_url


def get_followed_accounts_of_user(user_id: str):
    url = "https://spclient.wg.spotify.com/user-profile-view/v3/profile/{params[user_id]}/following?market=from_token"

    params = {"user_id": user_id}

    print(f"getting followed accounts of {user_id}")

    return get_data_from_url(url, params)


def save_followed_accounts_of_user(user_id: str):
    followed_accounts = get_followed_accounts_of_user(user_id)

    if followed_accounts:
        try:
            print(followed_accounts[0])
            # account = Result(
            #     url=url,
            #     result_all=raw_word_count,
            #     result_no_stop_words=no_stop_words_count
            # )
            # db.session.add(result)
            # db.session.commit()
        except:
            print("Unable to add item to database.")
    else:
        print(f"Didn't find any accounts user {user_id} follows!")
