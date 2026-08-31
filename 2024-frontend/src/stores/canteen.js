import { defineStore } from "pinia"
import { ref } from "vue"
import canteenService from "@/services/canteens.js"

const useStoreCanteen = defineStore("canteen", () => {
  const canteenInformations = ref(null)
  const canteenSavedId = ref(null)

  /* Init store with canteen informations */
  async function initStore(canteenId) {
    if (canteenSavedId.value === canteenId) return
    const canteen = await canteenService.fetchCanteen(canteenId)
    canteenInformations.value = {
      ...canteen,
      isGroupe: canteen.productionType === "groupe",
    }
    canteenSavedId.value = canteenId
  }

  /* Empty store */
  function deleteStore() {
    canteenInformations.value = null
    canteenSavedId.value = null
  }

  return {
    canteenInformations,
    initStore,
    deleteStore,
  }
})

export { useStoreCanteen }
