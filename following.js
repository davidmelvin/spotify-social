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

    
    const following = await buddyList.getFollowedAccountsForUserID(accessToken, "fzzfawpi8ustfwtikooal0ijm");

    const myArtists = await spotifyAPI.getFollowedArtists({limit: 1}).then(
        function (data) {
            return data.body.artists.items
        },
        function (err) {
            console.error(err);
        }
    )

  console.log(myArtists);
}



main()

// Run every minute
// setInterval(() => main(), 1000 * 60)
