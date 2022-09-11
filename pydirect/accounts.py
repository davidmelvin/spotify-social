import requests
from urllib.error import HTTPError

from credentials import api_access_token
from utils.requests import get_data_from_url


def get_followed_accounts_of_user(user_id: str):
    url = "https://spclient.wg.spotify.com/user-profile-view/v3/profile/{params[user_id]}/following?market=from_token"

    params = {"user_id": user_id}

    print(f"getting followed accounts of {user_id}")

    return get_data_from_url(url, params)
