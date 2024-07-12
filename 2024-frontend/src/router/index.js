import { createRouter, createWebHistory } from "vue-router"
import DiagnosticTunnel from "@/views/DiagnosticTunnel"

const routes = [
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

export default router
