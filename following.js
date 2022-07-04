const SpotifyWebApi = require("spotify-web-api-node");
const buddyList = require("./");
require("dotenv").config();
const fs = require("fs");

const myFollowedProfilesFileLocation =
  __dirname + "/data/myFollowedProfiles.json";

async function getMyFollowedProfiles(accessToken) {
  const me = await buddyList.getFollowedAccountsForUserID(
    accessToken,
    "kf4ls52nbna2ooyvj9k2ixzgb"
  );

  fs.writeFile(
    myFollowedProfilesFileLocation,
    JSON.stringify(me, null, 2),
    function (err) {
      if (err) {
        return console.error(err);
      }
    }
  );
}

function getMyFriendData() {
  const rawData = fs.readFileSync(myFollowedProfilesFileLocation);
  let friendData = JSON.parse(rawData).profiles;

  const friendsIFollow = friendData.filter(function (profile) {
    return profile.uri.startsWith("spotify:user");
  });

  friendDataAugmented = friendsIFollow.map(function (profile) {
    id = profile.uri.split(":").pop();
    return { ...profile, userID: id };
  });

  return friendDataAugmented;
}

function getMyArtistData() {
  const rawData = fs.readFileSync(myFollowedProfilesFileLocation);
  let friendData = JSON.parse(rawData).profiles;

  const artistsIFollow = friendData.filter(function (profile) {
    return profile.uri.startsWith("spotify:artist");
  });

  artistDataAugmented = artistsIFollow.map(function (profile) {
    return { ...profile, friends_who_follow: [] };
  });

  return artistDataAugmented;
}

async function main() {
  const spDcCookie = process.env.SP_DC_COOKIE;
  const { accessToken } = await buddyList.getWebAccessToken(spDcCookie);

  const spotifyAPI = buddyList.wrapWebApi(
    new SpotifyWebApi({ spDcCookie: process.env.SP_DC_COOKIE })
  );
  const tokenResponse = await spotifyAPI.getWebAccessToken();
  spotifyAPI.setAccessToken(tokenResponse.body.accessToken);

  //   await getMyFollowedProfiles(accessToken);
  const myFriendData = getMyFriendData();
  console.log(myFriendData.length);

  const myArtistData = getMyArtistData();
  console.log(myArtistData.length);

  //   for (const profile of friendData) {
  //     console.log(`Getting profiles followed by: ${profile.name}...`);
  //     const profilesFollowedByFriend =
  //       await buddyList.getFollowedAccountsForUserID(accessToken, profile.userID);

  //   }

  // for (const profile of friendData) {
  //     console.log(`Getting profiles followed by: ${profile.name}...`)
  //     const profilesFollowedByFriend = await buddyList.getFollowedAccountsForUserID(accessToken, profile.userID)

  //     const profilesInCommon = profilesFollowedByFriend.profiles.filter(function (account) {
  //         return account.is_following;
  //     })
  //     const artistsInCommon = profilesInCommon.filter(function (profile) {
  //         return profile.uri.startsWith("spotify:artist")
  //     });
  //     const friendsInCommon = profilesInCommon.filter(function (profile) {
  //         return profile.uri.startsWith("spotify:user")
  //     });
  //     console.log(`${profile.name} -- Arists in common: ${artistsInCommon.length}. Friends in common: ${friendsInCommon.length}.`)

  //     await new Promise(r => setTimeout(r, 2000));
  // }
}

main();
