import { defineStore } from "pinia"
import { computed, ref } from "vue"
import campaignService from "@/services/campaigns.js"

const useStoreCampaignDates = defineStore("campaignDates", () => {
  const isLoaded = ref(false)
  const allCampaignsInformations = ref({})
  const currentCampaignYear = Number(window.TELEDECLARATION_YEAR)
  const currentCampaignInformations = computed(() => allCampaignsInformations.value[currentCampaignYear] || {})
  const currentCampaignIsOpen = computed(() => {
    const { inTeledeclaration, inCorrection } = currentCampaignInformations.value
    return inTeledeclaration || inCorrection || false
  })

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
    isLoaded.value = false
  }

  return {
    allCampaignsInformations,
    currentCampaignYear,
    currentCampaignInformations,
    currentCampaignIsOpen,
    initStore,
    deleteStore,
  }
})

export { useStoreCampaignDates }
