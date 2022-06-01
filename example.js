const buddyList = require('./')
require('dotenv').config()


async function main () {
  const spDcCookie = process.env.SP_DC_COOKIE

  const { accessToken } = await buddyList.getWebAccessToken(spDcCookie)
  const friendActivity = await buddyList.getFriendActivity(accessToken)

  console.log(JSON.stringify(friendActivity, null, 2))
}



main()

// Run every minute
// setInterval(() => main(), 1000 * 60)
