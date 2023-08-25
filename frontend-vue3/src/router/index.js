import { createRouter, createWebHistory } from "vue-router"
import LandingPage from "@/views/LandingPage"
import AccessibilityDeclaration from "@/views/AccessibilityDeclaration"

const routes = [
  // {
  //   path: "/",
  //   meta: {
  //     home: true,
  //   },
  // },
  {
    // path: "/accueil",
    path: "/",
    name: "LandingPage",
    component: LandingPage,
  },
  {
    path: "/a11y",
    name: "AccessibilityDeclaration",
    component: AccessibilityDeclaration,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to /*, from, savedPosition*/) {
    if (to.hash) return { selector: to.hash, offset: { y: 200 } }
    // if (to.name === from.name && this.app.$vuetify.breakpoint.mdAndUp) return savedPosition
    return { x: 0, y: 0 }
  },
})

export { router, routes }
