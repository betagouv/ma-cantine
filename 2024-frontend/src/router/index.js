import { createRouter, createWebHistory } from "vue-router"
import WasteMeasurementTunnel from "@/views/WasteMeasurementTunnel"
import { useRootStore } from "../stores/root"

const routes = [
  {
    path: "/pesage-gaspillage-alimentaire/:canteenUrlComponent/:id?",
    name: "WasteMeasurementTunnel",
    component: WasteMeasurementTunnel,
    props: (route) => ({ ...route.query, ...route.params }),
    meta: {
      title: "Pesage gaspillage alimentaire",
      authenticationRequired: true,
      fullscreen: true,
    },
  },
]

const VUE3_PREFIX = "/v2"
routes.forEach((r) => {
  r.path = VUE3_PREFIX + r.path
})

const vue2Routes = [
  {
    path: "/",
    name: "Vue2Home",
  },
  {
    path: "/ma-progression/:canteenUrlComponent/:year/:measureId",
    name: "MyProgress",
  },
]
routes.push(...vue2Routes)

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  if (!to.path.startsWith(VUE3_PREFIX)) {
    location.href = location.origin + to.path
    return
  }
  const store = useRootStore()
  if (!store.initialDataLoaded) {
    store.fetchInitialData().then(() => {
      if (!store.loggedUser && to.meta.authenticationRequired) {
        next({ name: "Vue2Home", replace: true })
      } else {
        next()
      }
    })
  }
})

export default router
