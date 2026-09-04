import { defineStore } from "pinia"
import { ref } from "vue"
import canteenService from "@/services/canteens.js"

const useStoreCanteen = defineStore("canteen", () => {
  const canteenInformations = ref(null)

  /* Init store with canteen informations */
  async function initStore(canteenId) {
    const canteen = await canteenService.fetchCanteen(canteenId)
    canteenInformations.value = {
      ...canteen,
      isGroupe: canteen.productionType === "groupe",
    }
    return canteen
  }

  /* Empty store */
  function deleteStore() {
    canteenInformations.value = null
  }

  return {
    canteenInformations,
    initStore,
    deleteStore,
  }
})

export { useStoreCanteen }
