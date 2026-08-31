import { defineStore } from "pinia"
import { ref } from "vue"
import purchaseService from "@/services/purchases.js"

const useStorePurchaseSummary = defineStore("purchaseSummary", () => {
  const purchaseSummary = ref({})

  /* Init store with purchases summary */
  async function initStore(canteenId) {
    const lastYear = new Date().getFullYear() - 1  // Last year only for now
    const summary = await purchaseService.fetchPurchasesSummary(canteenId, lastYear)
    purchaseSummary.value[lastYear] = summary
  }

  /* Empty store */
  function deleteStore() {
    purchaseSummary.value = {}
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
  }
})

export { useStorePurchaseSummary }
