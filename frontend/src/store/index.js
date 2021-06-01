import Vue from "vue"
import Vuex from "vuex"
import Constants from "@/constants"

Vue.use(Vuex)

const headers = {
  "X-CSRFToken": window.CSRF_TOKEN || "",
  "Content-Type": "application/json",
}

const LOCAL_STORAGE_VERSION = "1"
const LOCAL_STORAGE_KEY = `diagnosis-local-${LOCAL_STORAGE_VERSION}`

const verifyResponse = function(response) {
  if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
  return response.json()
}

export default new Vuex.Store({
  state: {
    userLoadingStatus: Constants.LoadingStatus.IDLE,
    blogLoadingStatus: Constants.LoadingStatus.IDLE,
    canteensLoadingStatus: Constants.LoadingStatus.IDLE,

    sectors: [],
    publishedCanteens: [],
    userCanteens: [],
    initialDataLoaded: false,
    blogPosts: null,
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
    SET_PUBLISHED_CANTEENS(state, publishedCanteens) {
      state.publishedCanteens = publishedCanteens
    },
    SET_USER_CANTEENS(state, userCanteens) {
      state.userCanteens = userCanteens
    },
    UPDATE_USER_CANTEEN(state, userCanteen) {
      const canteenIndex = state.userCanteens.findIndex((x) => x.id === userCanteen.id)
      if (canteenIndex > -1) state.userCanteens.splice(canteenIndex, 1, userCanteen)
    },
    UPDATE_DIAGNOSIS(state, { canteenId, diagnosis }) {
      const canteen = state.userCanteens.find((x) => x.id === canteenId)
      const diagnosisIndex = canteen.diagnosis.findIndex((x) => x.id === diagnosis.id)
      if (diagnosisIndex > -1) canteen.diagnosis.splice(diagnosisIndex, 1, diagnosis)
    },
    SET_BLOG_POSTS(state, blogPosts) {
      state.blogPosts = blogPosts
    },
    SET_INITIAL_DATA_LOADED(state) {
      state.initialDataLoaded = true
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

    fetchPublishedCanteens(context) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch("/api/v1/publishedCanteens/")
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_PUBLISHED_CANTEENS", response)
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

    fetchBlogPosts(context) {
      context.commit("SET_BLOG_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch("/api/v1/blogPosts/")
        .then(verifyResponse)
        .then((response) => {
          context.commit("SET_BLOG_POSTS", response)
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
      return Promise.all([
        context.dispatch("fetchLoggedUser"),
        context.dispatch("fetchPublishedCanteens"),
        context.dispatch("fetchSectors"),
      ])
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

    updateCanteen(context, { id, payload }) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteens/${id}`, { method: "PATCH", headers, body: JSON.stringify(payload) })
        .then(verifyResponse)
        .then((response) => {
          context.commit("UPDATE_USER_CANTEEN", response)
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    updateDiagnosis(context, { canteenId, id, payload }) {
      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteens/${canteenId}/diagnosis/${id}`, {
        method: "PATCH",
        headers,
        body: JSON.stringify(payload),
      })
        .then(verifyResponse)
        .then((response) => {
          context.commit("UPDATE_DIAGNOSIS", { canteenId, diagnosis: response })
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
    },

    saveLocalStorageDiagnosis(context, diagnosis) {
      let savedDiagnosis = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY) || "{}")
      savedDiagnosis[diagnosis.year] = diagnosis
      localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(savedDiagnosis))
    },

    publishCanteen(context, canteenId) {
      const payload = {
        dataIsPublic: true,
        public: true,
      }

      context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
      return fetch(`/api/v1/canteens/${canteenId}`, { method: "PATCH", headers, body: JSON.stringify(payload) })
        .then(verifyResponse)
        .then((response) => {
          context.commit("UPDATE_USER_CANTEEN", response)
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.LOADING)
        })
        .catch((e) => {
          context.commit("SET_CANTEENS_LOADING_STATUS", Constants.LoadingStatus.ERROR)
          throw e
        })
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
  },

  getters: {
    getLocalDiagnosis: () => () => {
      const savedDiagnosis = localStorage.getItem(LOCAL_STORAGE_KEY)
      if (!savedDiagnosis) {
        return [
          Object.assign({}, Constants.DefaultDiagnostics, { year: 2019 }),
          Object.assign({}, Constants.DefaultDiagnostics, { year: 2020 }),
        ]
      }
      return Object.values(JSON.parse(savedDiagnosis))
    },
  },
})
