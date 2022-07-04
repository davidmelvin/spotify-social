const fetch = require('node-fetch')

exports.getWebAccessToken = async function getWebAccessToken (spDcCookie) {
  const res = await fetch('https://open.spotify.com/get_access_token?reason=transport&productType=web_player', {
    headers: {
      Cookie: `sp_dc=${spDcCookie}`
    }
  })

  return res.json()
}

exports.getFriendActivity = async function getFriendActivity (webAccessToken) {
  // Looks like the app now uses `https://spclient.wg.spotify.com/presence-view/v1/buddylist`
  // but both endpoints appear to be identical in the kind of token they accept
  // and the response format.
  const res = await
    fetch('https://guc-spclient.spotify.com/presence-view/v1/buddylist', {
    headers: {
      Authorization: `Bearer ${webAccessToken}`
    }
  })

  return res.json()
}

exports.getFollowedAccountsForUserID = async function foo (webAccessToken, userID) {
  const res = await
    fetch(`https://spclient.wg.spotify.com/user-profile-view/v3/profile/${userID}/following?market=from_token`, {
    headers: {
      Authorization: `Bearer ${webAccessToken}`
    }
  })

  return res.json()
}

exports.wrapWebApi = function wrapWebApi (api) {
  const Request = require('spotify-web-api-node/src/base-request')
  const HttpManager = require('spotify-web-api-node/src/http-manager')

  api.getWebAccessToken = function getWebAccessToken (callback) {
    const { spDcCookie } = this.getCredentials()

    return Request.builder()
      .withHost('open.spotify.com')
      .withPort(443)
      .withScheme('https')
      .withPath('/get_access_token')
      .withQueryParameters({
        reason: 'transport',
        productType: 'web_player'
      })
      .withHeaders({
        Accept: 'application/json',
        Cookie: `sp_dc=${spDcCookie}`,
        "User-Agent": 'Mozilla/5.0'
      })
      .build()
      .execute(HttpManager.get, callback)
  }

  api.getFriendActivity = function getFriendActivity (callback) {
    return Request.builder()
      .withHost('guc-spclient.spotify.com')
      .withPort(443)
      .withScheme('https')
      .withAuth(this.getAccessToken())
      .withPath('/presence-view/v1/buddylist')
      .build()
      .execute(HttpManager.get, callback)
  }

  // https://spclient.wg.spotify.com/user-profile-view/v3/profile/fzzfawpi8ustfwtikooal0ijm/following?market=from_token is a way to list all users and artists someone is following

  api.getFollowedAccountsOfUser = function getFollowedAccountsOfUser (userId, callback) {
    return Request.builder()
      .withHost('spclient.wg.spotify.com')
      .withPort(443)
      .withScheme('https')
      .withAuth(this.getAccessToken())
      .withPath(`/user-profile-view/v3/profile/${userId}/following?market=from_token`)
      .build()
      .execute(HttpManager.get, callback)
  }

  return api
}


