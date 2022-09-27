from utils import requests

import logging

logger = logging.getLogger("concert_buddies")


def fetch_spotify_profile_of_user(user_id):
    url = "https://spclient.wg.spotify.com/user-profile-view/v3/profile/{params[user_id]}?market=from_token"

    params = {"user_id": user_id}

    print(f"getting user info of {user_id}")
    try:
        data = requests.get_data_from_url(url, params)
        if not data:
            logger.info(
                "got error trying to get followed accounts of user: %s", user_id)
            return None
        # print(data.json())

        logger.info("fetch_spotify_profile_of_user:\n %s", data)

        return data.json()
    except Exception as err:
        error = f"failed to return fetch_spotify_profile_of_user as JSON: {err}"
        logger.error(error)
        raise Exception(error)
