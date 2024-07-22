import { createRouter, createWebHistory } from "vue-router"
import HomeView from "../views/HomeView.vue"
import AboutView from "../views/AboutView.vue"

const routes = [
  {
    path: "/",
    name: "HomeView",
    component: HomeView,
  },
  {
    path: "/about",
    name: "AboutView",
    component: AboutView,
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
