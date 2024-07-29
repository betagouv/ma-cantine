import { defineStore } from "pinia"
import { ref } from "vue"
import { useFetch } from "@vueuse/core"

export const useRootStore = defineStore("root", () => {
  const loggedUser = ref(null)
  const initialDataLoaded = ref(false)

  const fetchInitialData = async () => {
    const { data } = await useFetch("/api/v1/initialData/").json()
    setLoggedUser(data.value.loggedUser)
    initialDataLoaded.value = true
  }

  const setLoggedUser = (userData) => {
    loggedUser.value = userData ? userData : null
  }

  return {
    loggedUser,
    fetchInitialData,
  }
})
