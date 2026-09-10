import { defineStore } from "pinia"
import { computed, ref } from "vue"
import purchaseService from "@/services/purchases.js"

const useStorePurchaseSummary = defineStore("purchaseSummary", () => {
  const purchaseSummary = ref(null)
  const canteenSavedId = ref(null)
  const lastYear = window.TELEDECLARATION_YEAR
  const hasPurchaseTotal = computed(() => {
    const total = purchaseSummary.value?.valeurTotale
    return total != null && total > 0
  })

  /* Init store with last year purchases summary */
  async function initStore(canteenId) {
    if (canteenSavedId.value === canteenId) return
    purchaseSummary.value = await purchaseService.fetchPurchasesSummary(canteenId, lastYear)
    canteenSavedId.value = canteenId
  }

  /* Force refresh store */
  function refreshStore() {
    canteenSavedId.value = null
  }

  /* Empty store */
  function deleteStore() {
    purchaseSummary.value = null
    canteenSavedId.value = null
  }

  return {
    purchaseSummary,
    hasPurchaseTotal,
    initStore,
    deleteStore,
    refreshStore,
  }
})

export { useStorePurchaseSummary }
