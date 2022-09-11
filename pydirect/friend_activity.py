from utils.requests import get_data_from_url


def get_friend_activity():
    url = "https://guc-spclient.spotify.com/presence-view/v1/buddylist"

    print("getting friend activity")

    return get_data_from_url(url)


# def get_friend_activity():
#     url =
#       api.getFriendActivity = function getFriendActivity(callback) {
#     return Request.builder()
#       .withHost("guc-spclient.spotify.com")
#       .withPort(443)
#       .withScheme("https")
#       .withAuth(this.getAccessToken())
#       .withPath("/presence-view/v1/buddylist")
#       .build()
#       .execute(HttpManager.get, callback);
