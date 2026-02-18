import { createRouter, createWebHistory } from "vue-router"
import { useRootStore } from "@/stores/root"
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
  redirect: { name: "GestionnaireCantineGroupeSatellites" },
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
  if (!to.path.startsWith(VUE3_PREFIX)) {
    location.href = location.origin + to.fullPath
    return false
  }
  const store = useRootStore()
  if (!store.initialDataLoaded) {
    await store.fetchInitialData()
  }
  if (!store.loggedUser && to.meta.authenticationRequired) {
    return { name: "Vue2Home", replace: true }
  }
})


export { router, routes }
