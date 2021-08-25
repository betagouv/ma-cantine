import Vue from "vue"
import Vuex from "vuex"
import Constants from "@/constants"

Vue.use(Vuex)

const headers = {
  "X-CSRFToken": window.CSRF_TOKEN || "",
  "Content-Type": "application/json",
}

const LOCAL_STORAGE_VERSION = "1"
const LOCAL_STORAGE_KEY = `diagnostics-local-${LOCAL_STORAGE_VERSION}`

const verifyResponse = function(response) {
  if (response.status < 200 || response.status >= 400) {
    throw new Error(`Error encountered : ${response}`)
  }

  const contentType = response.headers.get("content-type")
  const hasJSON = contentType && contentType.startsWith("application/json")

  return hasJSON ? response.json() : response.text()
}

export default new Vuex.Store({
  state: {
    loggedUser: null,

    userLoadingStatus: Constants.LoadingStatus.IDLE,
    blogLoadingStatus: Constants.LoadingStatus.IDLE,
    canteensLoadingStatus: Constants.LoadingStatus.IDLE,

    sectors: [],
    userCanteens: [],
    initialDataLoaded: false,

    blogPostCount: null,
    blogPosts: [],

    notification: {
      message: "",
      status: null,
      title: "",
    },
  },

  mutations: {
    SET_USER_LOADING_STATUS(state, status) {
      state.userLoadingStatus = status
    },
    SET_BLOG_LOADING_STATUS(state, status) {
      state.blogLoadingStatus = status
    },
    SET_CANTEENS_LOADING_STATUS(state, status) {
      state.canteensLoadingStatus = status
    },
    SET_LOGGED_USER(state, loggedUser) {
      state.loggedUser = loggedUser
    },
    SET_SECTORS(state, sectors) {
      state.sectors = sectors
    },
    SET_USER_CANTEENS(state, userCanteens) {
      state.userCanteens = userCanteens
    },
    ADD_USER_CANTEEN(state, userCanteen) {
      state.userCanteens.unshift(userCanteen)
    },
    ADD_USER_CANTEENS(state, userCanteens) {
      state.userCanteens = userCanteens.concat(state.userCanteens)
    },
    UPDATE_USER_CANTEEN(state, userCanteen) {
      const canteenIndex = state.userCanteens.findIndex((x) => x.id === userCanteen.id)
      if (canteenIndex > -1) state.userCanteens.splice(canteenIndex, 1, userCanteen)
    },
    UPDATE_USER_CANTEEN_MANAGERS(state, { canteenId, data }) {
      const canteenIndex = state.userCanteens.findIndex((x) => x.id === canteenId)
      if (canteenIndex > -1) {
        let userCanteen = state.userCanteens[canteenIndex]
        userCanteen.managers = data.managers
        userCanteen.managerInvitations = data.managerInvitations
      }
    },
    DELETE_USER_CANTEEN(state, canteenId) {
      const userCanteenIndex = state.userCanteens.findIndex((x) => x.id === canteenId)
      if (userCanteenIndex > -1) state.userCanteens.splice(userCanteenIndex, 1)
    },
    ADD_DIAGNOSTIC(state, { canteenId, diagnostic }) {
      const canteen = state.userCanteens.find((x) => x.id === canteenId)
      canteen.diagnostics.push(diagnostic)
    },
    UPDATE_DIAGNOSTIC(state, { canteenId, diagnostic }) {
      const canteen = state.userCanteens.find((x) => x.id === canteenId)
      const diagnosticIndex = canteen.diagnostics.findIndex((x) => x.id === diagnostic.id)
      if (diagnosticIndex > -1) canteen.diagnostics.splice(diagnosticIndex, 1, diagnostic)
    },
    ADD_BLOG_POSTS(state, { response, limit, offset }) {
      state.blogPosts.push({ ...response, limit, offset })
      state.blogPostCount = response.count
    },
    SET_INITIAL_DATA_LOADED(state) {
      state.initialDataLoaded = true
    },
    SET_NOTIFICATION(state, { message, title, status }) {
      state.notification.message = message
      state.notification.title = title
      state.notification.status = status
    },
    REMOVE_NOTIFICATION(state, message) {
      if (message && state.notification.message !== message) {
        // in case there was another notification in between, do not remove it
        return
      }
      state.notification.message = null
      state.notification.status = null
      state.notification.title = null
    },
  },

  actions: {
    fetchLoggedUser(context) {
      context.commit("SET_USER_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch("/api/v1/loggedUser/")
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_LOGGED_USER", response)
          context.commit("SET_USER_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
        })
        .catch(() => {
          context.commit("SET_USER_LOADING_STATUS", Constants.LoadingStatus.ERROR)
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
        .catch(() => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
        })
    },
    fetchUserCanteens(context) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch("/api/v1/canteens/")
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_USER_CANTEENS", response)
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
        })
        .catch(() => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
        })
    },

    fetchBlogPosts(context, { limit = 6, offset }) {
      context.commit("SET_BLOG_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/blogPosts/?limit=${limit}&offset=${offset}`)
        .then(verifyResponse)
        .then((response) => {
          context.commit("ADD_BLOG_POSTS", { response, limit, offset })
          context.commit("SET_BLOG_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
        })
        .catch(() => {
          context.commit("SET_BLOG_LOADING_STATUS", Constants.LoadingStatus.ERROR)
        })
    },

    setInitialDataLoaded(context) {
      return context.commit("SET_INITIAL_DATA_LOADED")
    },

    fetchInitialData(context) {
      return Promise.all([context.dispatch("fetchLoggedUser"), context.dispatch("fetchSectors")])
        .then(() => {
          if (context.state.loggedUser) return context.dispatch("fetchUserCanteens")
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
          context.commit("ADD_USER_CANTEEN", response)
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
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
          context.commit("UPDATE_USER_CANTEEN", response)
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    publishCanteen(context, { id, payload }) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/publishCanteens/${id}`, { method: "PATCH", headers, body: JSON.stringify(payload) })
        .then(verifyResponse)
        .then((response) => {
          context.commit("UPDATE_USER_CANTEEN", response)
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
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
          context.commit("DELETE_USER_CANTEEN", id)
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
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
          context.commit("ADD_DIAGNOSTIC", { canteenId, diagnostic: response })
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
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
          context.commit("UPDATE_DIAGNOSTIC", { canteenId, diagnostic: response })
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
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

    subscribeBetaTester(context, payload) {
      return fetch("/api/v1/subscribeBetaTester/", { method: "POST", headers, body: JSON.stringify(payload) }).then(
        verifyResponse
      )
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
          context.commit("UPDATE_USER_CANTEEN_MANAGERS", { canteenId, data: response })
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    sendCanteenEmail(context, payload) {
      return fetch("/api/v1/contactCanteen/", { method: "POST", headers, body: JSON.stringify(payload) }).then(
        verifyResponse
      )
    },

    removeManager(context, { canteenId, email }) {
      return fetch(`/api/v1/removeManager/`, {
        method: "POST",
        headers,
        body: JSON.stringify({ canteenId, email }),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("UPDATE_USER_CANTEEN_MANAGERS", { canteenId, data: response })
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    importDiagnostics(context, payload) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      let form = new FormData()
      form.append("file", payload.file)
      return fetch(`/api/v1/importDiagnostics/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": window.CSRF_TOKEN || "",
        },
        body: form,
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("ADD_USER_CANTEENS", response.canteens)
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.SUCCESS)
          return response
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    notify(context, { title, message, status }) {
      context.commit("SET_NOTIFICATION", { title, message, status })
      setTimeout(() => context.commit("REMOVE_NOTIFICATION", message), 4000)
    },
    notifyRequiredFieldsError(context) {
      const title = null
      const message = "Merci de vérifier les champs en rouge et réessayer"
      const status = "error"
      context.dispatch("notify", { title, message, status })
    },
    notifyServerError(context) {
      const title = "Oops !"
      const message =
        "Une erreur est survenue, vous pouvez réessayer plus tard ou nous contacter directement à contact@egalim.beta.gouv.fr"
      const status = "error"
      context.dispatch("notify", { title, message, status })
    },
    removeNotification(context) {
      context.commit("REMOVE_NOTIFICATION")
    },
  },

  getters: {
    getLocalDiagnostics: () => () => {
      const savedDiagnostics = localStorage.getItem(LOCAL_STORAGE_KEY)
      if (!savedDiagnostics) {
        return [
          Object.assign({}, Constants.DefaultDiagnostics, { year: 2019 }),
          Object.assign({}, Constants.DefaultDiagnostics, { year: 2020 }),
          Object.assign({}, Constants.DefaultDiagnostics, { year: 2021 }),
          Object.assign({}, Constants.DefaultDiagnostics, { year: 2022 }),
        ]
      }
      return Object.values(JSON.parse(savedDiagnostics))
    },
    getCanteenUrlComponent: () => (canteen) => {
      return `${canteen.id}--${canteen.name}`
    },
    getCanteenFromUrlComponent: (state) => (canteenUrlComponent) => {
      const canteenId = canteenUrlComponent.split("--")[0]
      return state.userCanteens.find((x) => x.id === parseInt(canteenId))
    },
  },
})
