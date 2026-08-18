import { defineStore } from "pinia"
import { ref } from "vue"
import purchaseService from "@/services/purchases.js"

const useStorePurchaseSummary = defineStore("purchaseSummary", () => {
  const purchaseSummary = ref({})

  /* Init store with purchases summary */
  async function initStore(canteenId, year) {
    const summary = await purchaseService.fetchPurchasesSummary(canteenId, year)
    if (year) purchaseSummary.value[year] = summary
    else {
      for (let i = 0; i < summary["results"].length; i++) {
        const resultYear = summary["results"][i].year
        purchaseSummary.value[resultYear] = summary["results"][i]
      }
    }
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
