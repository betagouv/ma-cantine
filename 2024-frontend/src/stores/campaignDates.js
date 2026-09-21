import { defineStore } from "pinia"
import { computed, ref } from "vue"
import campaignService from "@/services/campaigns.js"

const useStoreCampaignDates = defineStore("campaignDates", () => {
  const isLoaded = ref(false)
  const allCampaignsInformations = ref({})
  const currentCampaignYear = Number(window.TELEDECLARATION_YEAR)
  const currentCampaignInformations = computed(allCampaignsInformations.value[currentCampaignYear] || {})

  /* Init store with all campaigns dates */
  async function initStore() {
    if (isLoaded.value) return
    const campaignsDates = await campaignService.getCampaignDates()
    for (const campaign of campaignsDates) {
      allCampaignsInformations.value[campaign.year] = campaign
    }
    allCampaignsInformations.value[currentCampaignYear] = await campaignService.getCampaignDates(currentCampaignYear)
    isLoaded.value = true
  }

  /* Empty store */
  function deleteStore() {
    allCampaignsInformations.value = {}
    currentCampaignInformations.value = {}
    isLoaded.value = false
  }

  return {
    allCampaignsInformations,
    currentCampaignYear,
    currentCampaignInformations,
    initStore,
    deleteStore,
  }
})

export { useStoreCampaignDates }
