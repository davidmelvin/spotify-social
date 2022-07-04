const SpotifyWebApi = require('spotify-web-api-node');
const buddyList = require('./')
require('dotenv').config()


async function main () {
  const spDcCookie = process.env.SP_DC_COOKIE

  const { accessToken } = await buddyList.getWebAccessToken(spDcCookie)
//   const friendActivity = await buddyList.getFriendActivity(accessToken)

    const spotifyAPI = buddyList.wrapWebApi(new SpotifyWebApi({ spDcCookie: process.env.SP_DC_COOKIE }))
    const tokenResponse = await spotifyAPI.getWebAccessToken()
    spotifyAPI.setAccessToken(tokenResponse.body.accessToken)

    
    const other = await buddyList.getFollowedAccountsForUserID(accessToken, "pranavjain97");
    const me = await buddyList.getFollowedAccountsForUserID(accessToken, "kf4ls52nbna2ooyvj9k2ixzgb");

    // console.log(other)
    
    const artistsIFollow = me.profiles.filter(function (profile) {
        return profile.uri.startsWith("spotify:artist")
    });

    const friendsIFollow = me.profiles.filter(function (profile) {
        return profile.uri.startsWith("spotify:user")
    });

    // console.log(artistsIFollow.length)
    // for (const profile of friendsIFollow) {
    //     console.log(profile.uri)
    // }

    const overlap = other.profiles.filter(function(account) {
        return account.is_following;
    })

    console.log(overlap);
    console.log(`we both follow ${overlap.length} users`)
    for (const account of overlap) {
        console.log(account.name)
    }


}



main()

// Run every minute
// setInterval(() => main(), 1000 * 60)
