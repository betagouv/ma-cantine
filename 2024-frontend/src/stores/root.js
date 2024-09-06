import { defineStore } from "pinia"
import { ref, reactive } from "vue"
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
  // state
  const loggedUser = ref(null)
  const initialDataLoaded = ref(false)
  const canteenPreviews = ref([])
  const notifications = reactive([])

  // actions
  const fetchInitialData = () => {
    return useFetch("/api/v1/initialData/")
      .json()
      .then(({ data }) => {
        loggedUser.value = data.value.loggedUser
        canteenPreviews.value = data.value.canteenPreviews
        initialDataLoaded.value = true
      })
  }

  const notify = (notification) => {
    // a notification consists of: message, title, status, undoAction, undoMessage
    notification.id = Math.floor(Math.random() * 10000) // generate random 5 digit id
    notifications.push(notification)
  }
  const notifyRequiredFieldsError = () => {
    const title = null
    const message = "Merci de vérifier les champs en rouge et réessayer"
    const status = "error"
    notify({ title, message, status })
  }
  const notifyServerError = (error) => {
    const title = "Oops !"
    const message =
      error instanceof AuthenticationError
        ? "Votre session a expiré. Rechargez la page et reconnectez-vous pour continuer."
        : "Une erreur est survenue, vous pouvez réessayer plus tard ou nous contacter directement à support-egalim@beta.gouv.fr"
    const status = "error"
    notify({ title, message, status })
  }
  const removeNotification = (notification) => {
    const idx = notifications.indexOf(notification)
    if (idx > -1) notifications.splice(idx, 1)
  }

  const createWasteMeasurement = async (canteenId, payload) => {
    return fetch(`/api/v1/canteens/${canteenId}/wasteMeasurements/`, {
      method: "POST",
      headers,
      body: JSON.stringify(payload),
    }).then(verifyResponse)
  }

  const updateWasteMeasurement = async (canteenId, measurementId, payload) => {
    return fetch(`/api/v1/canteens/${canteenId}/wasteMeasurements/${measurementId}`, {
      method: "PATCH",
      headers,
      body: JSON.stringify(payload),
    }).then(verifyResponse)
  }

  return {
    // state
    initialDataLoaded,
    loggedUser,
    notifications,
    canteenPreviews,

    // actions
    fetchInitialData,
    createWasteMeasurement,
    updateWasteMeasurement,
    notify,
    notifyRequiredFieldsError,
    notifyServerError,
    removeNotification,
  }
})
