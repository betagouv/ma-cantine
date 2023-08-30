<template>
  <DsfrBreadcrumb :links="breadcrumbLinks" />
</template>

<script>
import { routes } from "@/router"

export default {
  name: "BreadcrumbsNav",
  props: {
    links: {
      type: Array, // objects of to & (optionally) title
      required: false,
    },
    title: {
      type: String,
      required: false,
    },
  },
  data() {
    let breadcrumbRoutes = JSON.parse(JSON.stringify(routes))
    // flatten routes for simplicity
    breadcrumbRoutes.forEach((r) => {
      if (r.children) {
        breadcrumbRoutes.push(...r.children)
      }
    })
    return {
      breadcrumbRoutes,
    }
  },
  computed: {
    homePage() {
      const loggedUser = this.$store.state.loggedUser
      if (loggedUser && loggedUser.isDev) return { name: "DeveloperPage" }
      if (loggedUser && !loggedUser.isDev) return { name: "ManagementPage" }
      return { name: "LandingPage" }
    },
    pageTitle() {
      return this.title || this.breadcrumbRoutes.find((r) => r.name === this.$route.name)?.meta?.title
    },
    breadcrumbLinks() {
      const homepage = { text: "Accueil", to: this.homePage }
      const links = [homepage]
      if (this.links) {
        this.links.forEach((link) => {
          if (!link.text) {
            link.text = this.breadcrumbRoutes.find((r) => r.name === link.to.name)?.meta?.title
          }
        })
        links.push(...this.links)
      }
      const thispage = { text: this.pageTitle }
      links.push(thispage)
      return links
    },
  },
}
</script>
