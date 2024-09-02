import { defineStore } from "pinia"
import { ref } from "vue"
import { useFetch } from "@vueuse/core"

export const useRootStore = defineStore("root", () => {
  const loggedUser = ref(null)
  const initialDataLoaded = ref(false)
  const canteenPreviews = ref([])

  const fetchInitialData = () => {
    return useFetch("/api/v1/initialData/")
      .json()
      .then(({ data }) => {
        loggedUser.value = data.value.loggedUser
        canteenPreviews.value = data.value.canteenPreviews
        initialDataLoaded.value = true
      })
  }

  return {
    initialDataLoaded,
    loggedUser,
    canteenPreviews,
    fetchInitialData,
  }
})
