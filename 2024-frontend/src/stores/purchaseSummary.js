import { defineStore } from "pinia"
import { ref } from "vue"
import purchaseService from "@/services/purchases.js"

const useStorePurchaseSummary = defineStore("purchaseSummary", () => {
  const purchaseSummary = ref(null)

  /* Init store with purchases summary */
  async function initStore(canteenId, year) {
    const summary = await purchaseService.fetchPurchasesSummary(canteenId, year)
    purchaseSummary.value = year ? { year: summary } : summary
    return purchaseSummary.value
  }

  /* Empty store */
  function deleteStore() {
    purchaseSummary.value = null
  }

  return {
    purchaseSummary,
    initStore,
    deleteStore,
  }
})

export { useStorePurchaseSummary }
