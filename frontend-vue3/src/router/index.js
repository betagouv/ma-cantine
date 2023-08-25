import { createRouter, createWebHistory } from "vue-router"

const routes = [
  {
    path: "/",
    meta: {
      home: true,
    },
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
