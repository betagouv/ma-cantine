import { createRouter, createWebHistory } from "vue-router"
import { useRootStore } from "@/stores/root"
import { useStoreDiagnostic } from "@/stores/diagnostic"
import { useStoreCanteen } from "@/stores/canteen"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary"
import urlService from "@/services/urls"

import vue3routes from "./vue3.js"
import vue2routes from "./vue2.js"

/* Join two frontend routes */
const VUE3_PREFIX = "/v2"
const routes = []
routes.push(...vue3routes)
vue3routes.forEach((r) => {
  r.path = VUE3_PREFIX + r.path
})
routes.push(...vue2routes)

/* Redirects */
routes.push({
  path: "/v2/tableau-de-bord/cantines/:canteenUrlComponent/satellites/ajouter",
  redirect: { name: "GestionnaireCantineGroupe" },
})

/* Create router */
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to) {
    if (to.params.keepScrollPosition) return to
    const scrollTo = to.hash || "#app"
    const scrollTop = to.params.scrollTop || 0
    return { el: scrollTo, top: scrollTop }
  },
})

/* Middleware */
router.beforeEach(async (to) => {
  // Redirect to Vue3 if not on Vue3 prefix
  if (!to.path.startsWith(VUE3_PREFIX)) {
    location.href = location.origin + to.fullPath
    return false
  }
  // Fetch initial data
  const store = useRootStore()
  if (!store.initialDataLoaded) {
    await store.fetchInitialData()
  }
  // Verify user is logged in if required
  if (!store.loggedUser && to.meta.authenticationRequired) {
    return { name: "Vue2Home", replace: true }
  }
  // Load stores if required
  if (to.meta.storesRequired) {
    const canteenUrl = to.params.canteenUrlComponent
    const canteenId = urlService.getCanteenId(canteenUrl)
    const canteenStore = useStoreCanteen()
    const diagnosticStore = useStoreDiagnostic()
    const purchaseSummaryStore = useStorePurchaseSummary()
    if (to.meta.storesRequired.includes("canteen")) await canteenStore.initStore(canteenId)
    if (to.meta.storesRequired.includes("diagnostic")) await diagnosticStore.initStore(canteenId)
    if (to.meta.storesRequired.includes("purchaseSummary")) await purchaseSummaryStore.initStore(canteenId)
  }
})


export { router, routes }
