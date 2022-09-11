import requests
from urllib.error import HTTPError


from credentials import api_access_token


def get_data_from_url(url: str, params: dict[str, str] = None) -> dict:
    url = url.format(params=params)
    print(url)
    try:
        response = requests.get(
            url, headers={'Authorization': 'Bearer {}'.format(api_access_token)})

    except HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Unkown error: {err}')
    else:
        return response.json()
