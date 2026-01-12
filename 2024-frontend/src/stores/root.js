import { defineStore } from "pinia"
import { ref, reactive } from "vue"
import { useFetch } from "@vueuse/core"
import { verifyResponse, getDefaultErrorMessage } from "@/services/api.js"

const headers = {
  "X-CSRFToken": window.CSRF_TOKEN || "",
  "Content-Type": "application/json",
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

  const fetchCanteen = (id) => {
    return fetch(`/api/v1/canteens/${id}`)
      .then(verifyResponse)
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
    const title = error.title || "Erreur"
    const message = error.message || getDefaultErrorMessage()
    const status = error.status || "error"
    notify({ title, message, status })
  }
  const removeNotification = (notification) => {
    const idx = notifications.indexOf(notification)
    if (idx > -1) notifications.splice(idx, 1)
  }
  const removeNotifications = () => {
    notifications.splice(0)
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

  const sendInquiryEmail = async (payload) => {
    return fetch("/api/v1/inquiry/", {
      method: "POST",
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
    fetchCanteen,
    createWasteMeasurement,
    updateWasteMeasurement,
    notify,
    notifyRequiredFieldsError,
    notifyServerError,
    removeNotification,
    removeNotifications,
    sendInquiryEmail,
  }
})
