import { defineStore } from "pinia"
import { ref } from "vue"
import purchaseService from "@/services/purchases.js"

const useStorePurchaseSummary = defineStore("purchaseSummary", () => {
  const purchaseSummary = ref({})
  const canteenSavedId = ref(null)

  /* Init store with purchases summary */
  async function initStore(canteenId) {
    if (canteenSavedId.value === canteenId) return
    const lastYear = new Date().getFullYear() - 1  // Last year only for now
    const summary = await purchaseService.fetchPurchasesSummary(canteenId, lastYear)
    purchaseSummary.value[lastYear] = summary
    canteenSavedId.value = canteenId
  }

  /* Force refresh store */
  function refreshStore() {
    canteenSavedId.value = null
  }

  /* Empty store */
  function deleteStore() {
    purchaseSummary.value = {}
    canteenSavedId.value = null
  }

  /* Check if has purchase */
  function hasPurchaseTotal(year) {
    return purchaseSummary.value[year]?.valeurTotale && purchaseSummary.value[year]?.valeurTotale > 0
  }

  return {
    purchaseSummary,
    initStore,
    deleteStore,
    hasPurchaseTotal,
    refreshStore,
  }
})

export { useStorePurchaseSummary }
