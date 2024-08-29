import { defineStore } from "pinia"
import { ref } from "vue"
import { useFetch } from "@vueuse/core"
import { AuthenticationError, BadRequestError } from "../utils"

const headers = {
  "X-CSRFToken": window.CSRF_TOKEN || "",
  "Content-Type": "application/json",
}

const verifyResponse = function(response) {
  const contentType = response.headers.get("content-type")
  const hasJSON = contentType && contentType.startsWith("application/json")

  if (response.status < 200 || response.status >= 400) {
    if (response.status === 403) throw new AuthenticationError()
    else if (response.status === 400) {
      if (hasJSON) {
        throw new BadRequestError(response.json())
      } else {
        throw new BadRequestError()
      }
    } else throw new Error(`API responded with status of ${response.status}`)
  }

  return hasJSON ? response.json() : response.text()
}

export const useRootStore = defineStore("root", () => {
  // TODO: refactor to put in a state dict
  const loggedUser = ref(null)
  const initialDataLoaded = ref(false)

  // TODO: refacto to put this in actions
  const fetchInitialData = async () => {
    const { data } = await useFetch("/api/v1/initialData/").json()
    setLoggedUser(data.value.loggedUser)
    initialDataLoaded.value = true
  }

  const setLoggedUser = (userData) => {
    loggedUser.value = userData ? userData : null
  }

  const actions = {
    async createWasteMeasurement(canteenId, payload) {
      return fetch(`/api/v1/canteens/${canteenId}/wasteMeasurements/`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
      }).then(verifyResponse)
    },
  }

  return {
    loggedUser,
    fetchInitialData,
    actions,
  }
})
