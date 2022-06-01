require('dotenv').config()

const SpotifyWebApi = require('spotify-web-api-node')
const buddyList = require('./')

async function main() {
    const api = buddyList.wrapWebApi(new SpotifyWebApi({ spDcCookie: process.env.SP_DC_COOKIE }))

    const tokenResponse = await api.getWebAccessToken()
    api.setAccessToken(tokenResponse.body.accessToken)

    const friendActivityResponse = await api.getFriendActivity()
    const friendActivity = friendActivityResponse.body

    // console.log(JSON.stringify(friendActivity, null, 2))

    // Get Elvis' albums
    api.getFollowedArtists(
        {
            limit: 50,
            // cursors: {
            //     after:
            //         '1YIhBsaTuStHsl8wiSIgxo'
            // }
        }
    ).then(
        function (data) {
            console.log('Artist albums', data.body.artists.items);
        },
        function (err) {
            console.error(err);
        }
    );

}

main()