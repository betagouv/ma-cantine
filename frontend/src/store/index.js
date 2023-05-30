import Vue from "vue"
import Vuex from "vuex"
import Constants from "@/constants"
import { diagnosticYears, AuthenticationError, BadRequestError } from "../utils"

Vue.use(Vuex)

const headers = {
  "X-CSRFToken": window.CSRF_TOKEN || "",
  "Content-Type": "application/json",
}

const LOCAL_STORAGE_VERSION = "1"
const LOCAL_STORAGE_KEY = `diagnostics-local-${LOCAL_STORAGE_VERSION}`

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

export default new Vuex.Store({
  state: {
    loggedUser: null,
    pageTitleSuffix: "ma cantine",

    userLoadingStatus: Constants.LoadingStatus.IDLE,
    canteensLoadingStatus: Constants.LoadingStatus.IDLE,
    purchasesLoadingStatus: Constants.LoadingStatus.IDLE,
    expeLoadingStatus: Constants.LoadingStatus.IDLE,
    communityEventsLoadingStatus: Constants.LoadingStatus.IDLE,
    videoTutorialsLoadingStatus: Constants.LoadingStatus.IDLE,

    sectors: [],
    sectorCategories: [],
    userCanteenPreviews: [],
    initialDataLoaded: false,
    upcomingCommunityEvents: [],
    videoTutorials: [],

    notification: {
      message: "",
      status: null,
      title: "",
    },

    showWebinaireBanner: false,
  },

  mutations: {
    SET_USER_LOADING_STATUS(state, status) {
      state.userLoadingStatus = status
    },
    SET_CANTEENS_LOADING_STATUS(state, status) {
      state.canteensLoadingStatus = status
    },
    SET_PURCHASES_LOADING_STATUS(state, status) {
      state.purchasesLoadingStatus = status
    },
    SET_EXPE_LOADING_STATUS(state, status) {
      state.expeLoadingStatus = status
    },
    SET_COMMUNITY_EVENTS_LOADING_STATUS(state, status) {
      state.communityEventsLoadingStatus = status
    },
    SET_VIDEO_TUTORIALS_LOADING_STATUS(state, status) {
      state.videoTutorialsLoadingStatus = status
    },
    SET_LOGGED_USER(state, loggedUser) {
      state.loggedUser = loggedUser
    },
    SET_SECTORS(state, sectors) {
      state.sectors = sectors
      state.sectorCategories = []
      state.sectors.forEach((s) => {
        if (!s.category) s.category = "inconnu"
        if (state.sectorCategories.indexOf(s.category) === -1) {
          state.sectorCategories.push(s.category)
        }
      })
      // alphabetical order with other and unknown at the bottom
      state.sectorCategories.sort((a, b) => {
        if (a === b) return 0
        if (a === "inconnu") return 1
        else if (b === "inconnu") return -1
        else if (a === "autres") return 1
        else if (b === "autres") return -1
        else if (a < b) return -1
        else if (a > b) return 1
      })
    },
    SET_USER_CANTEEN_PREVIEWS(state, userCanteenPreviews) {
      state.userCanteenPreviews = userCanteenPreviews
    },
    SET_INITIAL_DATA_LOADED(state) {
      state.initialDataLoaded = true
    },
    SET_NOTIFICATION(state, { message, title, status, undoAction, undoMessage }) {
      state.notification.message = message
      state.notification.title = title
      state.notification.status = status
      state.notification.undoAction = undoAction
      state.notification.undoMessage = undoMessage
    },
    ADD_CANTEEN(state, canteen) {
      state.userCanteenPreviews.push({
        id: canteen.id,
        name: canteen.name,
      })
    },
    UPDATE_CANTEEN(state, canteen) {
      const storedCanteen = state.userCanteenPreviews.find((x) => x.id === canteen.id)
      if (storedCanteen) storedCanteen.name = canteen.name
    },
    REMOVE_CANTEEN(state, id) {
      const index = state.userCanteenPreviews.findIndex((x) => x.id === id)
      state.userCanteenPreviews.splice(index, 1)
    },
    REMOVE_NOTIFICATION(state, message) {
      if (message && state.notification.message !== message) {
        // in case there was another notification in between, do not remove it
        return
      }
      state.notification.message = null
      state.notification.status = null
      state.notification.title = null
      state.notification.undoAction = null
      state.notification.undoMessage = null
    },
    SET_UPCOMING_COMMUNITY_EVENTS(state, events) {
      state.upcomingCommunityEvents = events
    },
    SET_VIDEO_TUTORIALS(state, events) {
      state.videoTutorials = events
    },
    SET_SHOW_WEBINAIRE_BANNER(state, showWebinaireBanner) {
      state.showWebinaireBanner = showWebinaireBanner
    },
  },

  actions: {
    fetchLoggedUser(context) {
      context.commit("SET_USER_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch("/api/v1/loggedUser/")
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_LOGGED_USER", response || null)
          context.commit("SET_USER_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          if (context.state.loggedUser && window.$crisp) {
            window.$crisp.push(["set", "user:email", [context.state.loggedUser.email]])
          }
        })
        .catch((e) => {
          console.error("fetchLoggedUser", e)
          context.commit("SET_USER_LOADING_STATUS", Constants.LoadingStatus.ERROR)
        })
    },

    // It is possible to implement a cache at this level
    fetchCanteen(context, { id }) {
      return fetch(`/api/v1/canteens/${id}`).then((response) => {
        if (response.status != 200) throw new Error()
        return response.json()
      })
    },

    fetchSectors(context) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch("/api/v1/sectors/")
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_SECTORS", response)
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
        })
        .catch((e) => {
          console.log("fetchSectors", e)
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
        })
    },

    fetchUserCanteenPreviews(context) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch("/api/v1/canteenPreviews/")
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_USER_CANTEEN_PREVIEWS", response)
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
        })
        .catch((e) => {
          console.log("fetchUserCanteenPreviews", e)
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
        })
    },

    fetchBlogPosts(context, { limit = 6, offset, tag }) {
      let url = `/api/v1/blogPosts/?limit=${limit}&offset=${offset}`
      if (tag) url += `&tag=${tag}`
      return fetch(url)
        .then(verifyResponse)
        .then((response) => {
          return response
        })
    },

    fetchInitialData(context) {
      return Promise.all([
        context.dispatch("fetchLoggedUser"),
        context.dispatch("fetchSectors"),
        context.dispatch("fetchUpcomingCommunityEvents"),
        context.dispatch("fetchVideoTutorials"),
      ])
        .then(() => {
          if (context.state.loggedUser) return context.dispatch("fetchUserCanteenPreviews")
        })
        .then(() => {
          const criticalLoadingStatuses = ["canteensLoadingStatus"]
          const hasError = criticalLoadingStatuses.some((x) => context.state[x] === Constants.LoadingStatus.ERROR)
          if (hasError) throw new Error("Une erreur s'est produite lors du chargement des données intiales")
          else context.commit("SET_INITIAL_DATA_LOADED")
        })
    },

    updateProfile(context, { payload }) {
      context.commit("SET_USER_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/user/${context.state.loggedUser.id}`, {
        method: "PATCH",
        headers,
        body: JSON.stringify(payload),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_LOGGED_USER", response)
          context.commit("SET_USER_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
        })
        .catch((e) => {
          context.commit("SET_USER_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    changePassword(context, { payload }) {
      context.commit("SET_USER_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch("/api/v1/passwordChange/", { method: "PUT", headers, body: JSON.stringify(payload) })
        .then((response) => {
          if (response.status === 400) {
            return response.json().then((jsonResponse) => {
              throw new Error(Object.values(jsonResponse).join(", "))
            })
          }
          return verifyResponse(response)
        })
        .then(() => {
          context.commit("SET_USER_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
        })
        .catch((e) => {
          context.commit("SET_USER_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    createCanteen(context, { payload }) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteens/`, { method: "POST", headers, body: JSON.stringify(payload) })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          context.commit("ADD_CANTEEN", response)
          return response
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    updateCanteen(context, { id, payload }) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteens/${id}`, { method: "PATCH", headers, body: JSON.stringify(payload) })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          context.commit("UPDATE_CANTEEN", response)
          return response
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    publishCanteen(context, { id, payload }) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteens/${id}/publish`, { method: "POST", headers, body: JSON.stringify(payload) })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    unpublishCanteen(context, { id, payload }) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteens/${id}/unpublish`, { method: "POST", headers, body: JSON.stringify(payload) })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    deleteCanteen(context, { id }) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteens/${id}`, { method: "DELETE", headers })
        .then(verifyResponse)
        .then(() => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          context.commit("REMOVE_CANTEEN", id)
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    createDiagnostic(context, { canteenId, payload }) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteens/${canteenId}/diagnostics/`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    updateDiagnostic(context, { canteenId, id, payload }) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteens/${canteenId}/diagnostics/${id}`, {
        method: "PATCH",
        headers,
        body: JSON.stringify(payload),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    saveLocalStorageDiagnostic(context, diagnostic) {
      let savedDiagnostics = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY) || "{}")
      savedDiagnostics[diagnostic.year] = diagnostic
      return localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(savedDiagnostics))
    },

    removeLocalStorageDiagnostics() {
      return localStorage.removeItem(LOCAL_STORAGE_KEY)
    },

    subscribeNewsletter(context, email) {
      return fetch("/api/v1/subscribeNewsletter/", { method: "POST", headers, body: JSON.stringify({ email }) }).then(
        verifyResponse
      )
    },

    addManager(context, { canteenId, email }) {
      return fetch(`/api/v1/addManager/`, {
        method: "POST",
        headers,
        body: JSON.stringify({ canteenId, email }),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    sendCanteenEmail(context, payload) {
      return fetch("/api/v1/message/", { method: "POST", headers, body: JSON.stringify(payload) }).then(verifyResponse)
    },

    sendCanteenNotFoundEmail(context, payload) {
      return fetch("/api/v1/canteenNotFoundMessage/", { method: "POST", headers, body: JSON.stringify(payload) }).then(
        verifyResponse
      )
    },

    sendCanteenTeamRequest(context, { canteenId, payload }) {
      return fetch(`/api/v1/teamJoinRequest/${canteenId}/`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
      }).then(verifyResponse)
    },

    removeManager(context, { canteenId, email }) {
      return fetch(`/api/v1/removeManager/`, {
        method: "POST",
        headers,
        body: JSON.stringify({ canteenId, email }),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    importDiagnostics(context, { importLevel, payload }) {
      let form = new FormData()
      form.append("file", payload.file)
      return fetch(`/api/v1/importDiagnostics/${importLevel === "COMPLETE" ? "complete" : "simple"}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": window.CSRF_TOKEN || "",
        },
        body: form,
      }).then(verifyResponse)
    },

    importPurchases(context, payload) {
      let form = new FormData()
      form.append("file", payload.file)
      return fetch(`/api/v1/importPurchases/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": window.CSRF_TOKEN || "",
        },
        body: form,
      }).then(verifyResponse)
    },

    notify(context, { title, message, status, undoAction, undoMessage, duration }) {
      context.commit("SET_NOTIFICATION", { title, message, status, undoAction, undoMessage })
      setTimeout(() => context.commit("REMOVE_NOTIFICATION", message), duration || 4000)
    },
    notifyRequiredFieldsError(context) {
      const title = null
      const message = "Merci de vérifier les champs en rouge et réessayer"
      const status = "error"
      context.dispatch("notify", { title, message, status })
    },
    notifyServerError(context, error) {
      const title = "Oops !"
      const message =
        error instanceof AuthenticationError
          ? "Votre session a expiré. Rechargez la page et reconnectez-vous pour continuer."
          : "Une erreur est survenue, vous pouvez réessayer plus tard ou nous contacter directement à support-egalim@beta.gouv.fr"
      const status = "error"
      context.dispatch("notify", { title, message, status })
    },
    removeNotification(context) {
      context.commit("REMOVE_NOTIFICATION")
    },

    submitTeledeclaration(context, { id }) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      const payload = {
        diagnosticId: id,
      }
      return fetch("/api/v1/teledeclaration/", {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
      })
        .then(verifyResponse)
        .then((diagnostic) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return diagnostic
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    // TODO: remove
    submitMultipleTeledeclarations(context, { ids }) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      const payload = {
        diagnosticIds: ids,
      }
      return fetch("/api/v1/teledeclaration/", {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    submitMultiplePublications(context, { ids }) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch("/api/v1/publish/", {
        method: "POST",
        headers,
        body: JSON.stringify({ ids }),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    cancelTeledeclaration(context, { id }) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/teledeclaration/${id}/cancel/`, {
        method: "POST",
        headers,
      })
        .then(verifyResponse)
        .then((diagnostic) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return diagnostic
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    sendInquiryEmail(_, payload) {
      return fetch("/api/v1/inquiry/", { method: "POST", headers, body: JSON.stringify(payload) }).then(verifyResponse)
    },

    createPurchase(context, { payload }) {
      context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/purchases/`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    updatePurchase(context, { id, payload }) {
      context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/purchases/${id}`, {
        method: "PATCH",
        headers,
        body: JSON.stringify(payload),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    deletePurchase(context, { id }) {
      context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/purchases/${id}`, {
        method: "DELETE",
        headers,
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    deletePurchases(context, { ids }) {
      context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/purchases/`, {
        method: "DELETE",
        headers,
        body: JSON.stringify({ ids }),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    restorePurchases(context, ids) {
      context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/purchases/restore/`, {
        method: "POST",
        headers,
        body: JSON.stringify({ ids }),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_PURCHASES_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    fetchReservationExpe(context, { canteen }) {
      context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteen/${canteen.id}/reservationExpe/`)
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    createReservationExpe(context, { canteen, payload }) {
      context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteen/${canteen.id}/reservationExpe/`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    updateReservationExpe(context, { canteen, payload }) {
      context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteen/${canteen.id}/reservationExpe/`, {
        method: "PATCH",
        headers,
        body: JSON.stringify(payload),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    fetchVegetarianExpe(context, { canteen }) {
      context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteen/${canteen.id}/vegetarianExpe/`)
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    createVegetarianExpe(context, { canteen, payload }) {
      context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteen/${canteen.id}/vegetarianExpe/`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    updateVegetarianExpe(context, { canteen, payload }) {
      context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteen/${canteen.id}/vegetarianExpe/`, {
        method: "PATCH",
        headers,
        body: JSON.stringify(payload),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_EXPE_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    createReview(context, { payload }) {
      return fetch("/api/v1/reviews/", { method: "POST", headers, body: JSON.stringify(payload) })
        .then(verifyResponse)
        .then((response) => {
          context.dispatch("fetchLoggedUser") // refresh reviews for user
          return response
        })
        .catch((e) => {
          throw e
        })
    },

    fetchUpcomingCommunityEvents(context) {
      context.commit("SET_COMMUNITY_EVENTS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch("/api/v1/communityEvents/")
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_UPCOMING_COMMUNITY_EVENTS", response)
          context.commit("SET_COMMUNITY_EVENTS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
        })
        .catch((e) => {
          console.log("fetchUpcomingCommunityEvents", e)
          context.commit("SET_COMMUNITY_EVENTS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    fetchVideoTutorials(context) {
      context.commit("SET_VIDEO_TUTORIALS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch("/api/v1/videoTutorials/")
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_VIDEO_TUTORIALS", response)
          context.commit("SET_VIDEO_TUTORIALS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
        })
        .catch((e) => {
          console.log("fetchVideoTutorials", e)
          context.commit("SET_VIDEO_TUTORIALS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    claimCanteen(context, { canteenId }) {
      return fetch(`/api/v1/canteens/${canteenId}/claim/`, { method: "POST", headers }).then(verifyResponse)
    },

    undoClaimCanteen(context, { canteenId }) {
      return fetch(`/api/v1/canteens/${canteenId}/undoClaim/`, { method: "POST", headers }).then(verifyResponse)
    },

    addSatellite(context, { id, payload }) {
      return fetch(`/api/v1/canteens/${id}/satellites/`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
      }).then((response) => {
        return response.json().then((jsonResponse) => {
          if (response.status < 200 || response.status >= 400) throw new Error(jsonResponse.detail)
          return jsonResponse
        })
      })
    },

    setShowWebinaireBanner(context, showWebinaireBanner) {
      context.commit("SET_SHOW_WEBINAIRE_BANNER", showWebinaireBanner)
    },
  },

  getters: {
    getLocalDiagnostics: () => () => {
      const savedDiagnostics = localStorage.getItem(LOCAL_STORAGE_KEY)
      if (!savedDiagnostics) {
        return diagnosticYears().map((year) => Object.assign({}, Constants.DefaultDiagnostics, { year }))
      }
      return Object.values(JSON.parse(savedDiagnostics))
    },
    getCanteenUrlComponent: () => (canteen) => {
      return `${canteen.id}--${canteen.name}`
    },
    getPartnerUrlComponent: () => (partner) => {
      return `${partner.id}--${partner.name}`
    },
  },
})
