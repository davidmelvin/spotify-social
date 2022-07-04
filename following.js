const SpotifyWebApi = require('spotify-web-api-node');
const buddyList = require('./')
require('dotenv').config()


async function main() {
    const spDcCookie = process.env.SP_DC_COOKIE
    const { accessToken } = await buddyList.getWebAccessToken(spDcCookie)

    const spotifyAPI = buddyList.wrapWebApi(new SpotifyWebApi({ spDcCookie: process.env.SP_DC_COOKIE }))
    const tokenResponse = await spotifyAPI.getWebAccessToken()
    spotifyAPI.setAccessToken(tokenResponse.body.accessToken)

    const me = await buddyList.getFollowedAccountsForUserID(accessToken, "kf4ls52nbna2ooyvj9k2ixzgb");

    const friendsIFollow = me.profiles.filter(function (profile) {
        return profile.uri.startsWith("spotify:user")
    });

    const friendData = friendsIFollow.map(function (profile) {
        id = profile.uri.split(":").pop()
        return { ...profile, userID: id }
    })

    for (const profile of friendData) {
        console.log(`Getting profiles followed by: ${profile.name}...`)
        const profilesFollowedByFriend = await buddyList.getFollowedAccountsForUserID(accessToken, profile.userID)

        const profilesInCommon = profilesFollowedByFriend.profiles.filter(function (account) {
            return account.is_following;
        })
        const artistsInCommon = profilesInCommon.filter(function (profile) {
            return profile.uri.startsWith("spotify:artist")
        });
        const friendsInCommon = profilesInCommon.filter(function (profile) {
            return profile.uri.startsWith("spotify:user")
        });
        console.log(`${profile.name} -- Arists in common: ${artistsInCommon.length}. Friends in common: ${friendsInCommon.length}.`)
        
        await new Promise(r => setTimeout(r, 2000));
    }

}

main()
