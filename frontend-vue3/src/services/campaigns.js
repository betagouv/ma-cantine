import { verifyResponse } from "@/services/api.js"

const getYearCampaignDates = (year) => {
  return fetch(`/api/v1/campaignDates/${year}/`, { method: "GET" })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

export default { getYearCampaignDates }
