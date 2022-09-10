import requests
from urllib.error import HTTPError

from credentials import api_access_token


def get_followed_accounts_of_user(user_id: str):
    url = "https://spclient.wg.spotify.com/user-profile-view/v3/profile/{}/following?market=from_token"

    try:
        response = requests.get(
            url.format(user_id), headers={'Authorization': 'Bearer {}'.format(api_access_token)})

    except HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Unkown error: {err}')
    else:
        return response.json()
