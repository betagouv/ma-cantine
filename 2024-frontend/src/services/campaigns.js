import { verifyResponse } from "@/services/api.js"

const getCampaignDates = (year) => {
  let url = "/api/v1/campaignDates/"
  if (year) url += `${year}/`
  return fetch(url, { method: "GET" })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

export default { getCampaignDates }
