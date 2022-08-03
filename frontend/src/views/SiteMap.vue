<template>
  <div class="text-left">
    <h1 class="font-weight-black my-8">Plan du site</h1>
    <v-row>
      <v-col v-for="group in sitemapGroups" :key="group.title" cols="6">
        <h2 class="my-2">{{ group.title }}</h2>
        <ul>
          <li v-for="link in group.links" :key="link.text">
            <router-link :to="{ name: link.name }" :href="link.path">
              {{ (link.meta || {}).title || link.name }}
            </router-link>
          </li>
        </ul>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { routes } from "@/router"
export default {
  name: "SiteMap",
  data() {
    const isAuthenticated = !!this.$store.state.loggedUser
    let sitemapRoutes = JSON.parse(JSON.stringify(routes))
    sitemapRoutes.forEach((r) => {
      if (r.children) {
        sitemapRoutes.push(...r.children)
      }
    })
    sitemapRoutes = sitemapRoutes.filter((route) => {
      const hasViewRights = route.meta?.authenticationRequired ? isAuthenticated : true
      return !!route.sitemapGroup && hasViewRights
    })
    return {
      sitemapGroups: [
        {
          title: "S'informer sur les lois",
          links: sitemapRoutes.filter((f) => f.sitemapGroup === "LAW"),
        },
        {
          title: "Se diagnostiquer",
          links: sitemapRoutes.filter((f) => f.sitemapGroup === "DIAG"),
        },
        {
          title: "Améliorer votre offre",
          links: sitemapRoutes.filter((f) => f.sitemapGroup === "ACTION"),
        },
        {
          title: "Informations sur le site",
          links: sitemapRoutes.filter((f) => f.sitemapGroup === "SITE"),
        },
      ],
    }
  },
}
</script>
