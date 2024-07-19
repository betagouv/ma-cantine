import { createRouter, createWebHistory } from "vue-router"
import DiagnosticTunnel from "@/views/DiagnosticTunnel"
import { useRootStore } from "../stores/root"

const routes = [
  {
    path: "/",
    name: "Vue2Home",
    meta: {
      redirectToVue2: true,
    },
  },
  {
    path: "/diagnostic-tunnel/:canteenUrlComponent/:year/:measureId",
    name: "DiagnosticTunnel",
    component: DiagnosticTunnel,
    props: (route) => ({ ...route.query, ...route.params }),
    meta: {
      title: "Bilan",
      authenticationRequired: true,
      fullscreen: true,
    },
  },
]

routes.forEach((r) => {
  r.path = "/v2" + r.path
})

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  if (to.meta.redirectToVue2) {
    location.href = location.origin
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
