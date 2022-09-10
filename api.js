require("dotenv").config();

const SpotifyWebApi = require("spotify-web-api-node");
const buddyList = require("./");

async function main() {
  const spotifyAPI = buddyList.wrapWebApi(
    new SpotifyWebApi({ spDcCookie: process.env.SP_DC_COOKIE })
  );

  const tokenResponse = await spotifyAPI.getWebAccessToken();
  spotifyAPI.setAccessToken(tokenResponse.body.accessToken);

  //   spotifyAPI
  // .getFollowedArtists({
  //   limit: 1,
  cursors: {
    after: "1YIhBsaTuStHsl8wiSIgxo";
  }
  // })
  // .then(
  //   function (data) {
  // console.log("My followed artists", data.body.artists.items);
  //   },
  //   function (err) {
  // console.error(err);
  //   }
  // );
}

async function getFollowedAccounts() {
  userID = "fzzfawpi8ustfwtikooal0ijm";

  await spotifyAPI.getFollowedAccountsOfUser(userID).then(
    function (data) {
      console.log(`User ${userID} is following:\n`, data.body.profiles[0].name);
      // userToFollowing[userID] = data.body
      return data.body;
    },
    function (err) {
      console.error(err);
    }
  );
}

main();
