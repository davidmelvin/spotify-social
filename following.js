const SpotifyWebApi = require("spotify-web-api-node");
const buddyList = require("./");
require("dotenv").config();
const fs = require("fs");
const utils = require("./utils");

const sharedArtistsFileLocation = __dirname + "/data/sharedArtists.json";
const myFollowedProfilesFileLocation =
  __dirname + "/data/myFollowedProfiles.json";

const myFriendsDataFolderLocation = __dirname + "/data/friends/";

async function getAndSaveMyFollowedProfiles(accessToken) {
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

  friendDataAugmented = {};

  for (const friend of friendsIFollow) {
    id = friend.uri.split(":").pop();
    friendDataAugmented[id] = friend;
  }
  //   friendDataAugmented = friendsIFollow.map(function (profile) {
  //     return { ...profile, userID: id };
  //   });

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

async function getAndSaveProfilesFollowedByMyFriends(friendData, accessToken) {
  const friendCount = Object.keys(friendData).length;
  let friendNum = 0;
  for (const [userID, profile] of Object.entries(friendData)) {
    console.log(
      `${friendNum}/${friendCount} Getting profiles followed by ${profile.name}...`
    );
    const profilesFollowedByFriend =
      await buddyList.getFollowedAccountsForUserID(accessToken, userID);

    fs.writeFile(
      myFriendsDataFolderLocation + userID + ".json",
      JSON.stringify(profilesFollowedByFriend.profiles, null, 2),
      function (err) {
        if (err) {
          return console.error(err);
        }
      }
    );

    friendNum += 1;

    await new Promise((r) => setTimeout(r, 50));
  }
}

function getFriendFileData() {
  // https://stackoverflow.com/questions/10049557/reading-all-files-in-a-directory-store-them-in-objects-and-send-the-object

  let friendsFollowedProfiles = {};
  utils.readFiles(
    myFriendsDataFolderLocation,
    function (filename, content) {
      if (content != "undefined") {
        key = filename.split(".")[0];
        friendsFollowedProfiles[key] = JSON.parse(content);
        //   console.log(friendsFollowedProfiles[key].length);
      }
    },
    console.err
  );

  return friendsFollowedProfiles;
}

function listFriendsbyArtist(friendData, friendsFollowedProfiles) {
  sharedArtists = {};
  for (const [friendUserID, followedProfiles] of Object.entries(
    friendsFollowedProfiles
  )) {
    if (!(friendUserID in friendData)) {
      console.log("missing friend user id, ", friendUserID);
      break;
    }
    if (friendUserID == "1297443575") {
      console.log("skipping myself");
      continue;
    }
    friendName = friendData[friendUserID].name;
    for (const profile of followedProfiles) {
      if (profile.is_following && profile.uri.startsWith("spotify:artist")) {
        if (profile.name in sharedArtists) {
          sharedArtists[profile.name].push(friendName);
        } else {
          sharedArtists[profile.name] = [friendName];
        }
      }
    }
  }

  return sharedArtists;
}
async function main() {
  const spDcCookie = process.env.SP_DC_COOKIE;
  const { accessToken } = await buddyList.getWebAccessToken(spDcCookie);

  const spotifyAPI = buddyList.wrapWebApi(
    new SpotifyWebApi({ spDcCookie: process.env.SP_DC_COOKIE })
  );
  const tokenResponse = await spotifyAPI.getWebAccessToken();
  spotifyAPI.setAccessToken(tokenResponse.body.accessToken);

  //   await saveMyFollowedProfiles(accessToken);
  const myFriendData = getMyFriendData();

  //   const myArtistData = getMyArtistData();
  //   console.log(myArtistData.length);

  //   getAndSaveProfilesFollowedByMyFriends(myFriendData, accessToken);
  const friendsFollowedProfiles = getFriendFileData();
  //   //   console.log(Object.keys(friendsFollowedProfiles));

  const sharedArtists = listFriendsbyArtist(
    myFriendData,
    friendsFollowedProfiles
  );

  //   console.log(sharedArtists);

  fs.writeFile(
    sharedArtistsFileLocation,
    JSON.stringify(sharedArtists, null, 2),
    function (err) {
      if (err) {
        return console.error(err);
      }
    }
  );
}

main();
