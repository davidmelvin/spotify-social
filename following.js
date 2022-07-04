const buddyList = require('./')
require('dotenv').config()


async function main () {
  const spDcCookie = process.env.SP_DC_COOKIE

  const { accessToken } = await buddyList.getWebAccessToken(spDcCookie)
//   const friendActivity = await buddyList.getFriendActivity(accessToken)


    const following = await buddyList.getFollowedAccountsForUserID(accessToken, "fzzfawpi8ustfwtikooal0ijm");

  console.log(following)
}



main()

// Run every minute
// setInterval(() => main(), 1000 * 60)
