<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <h1 class="font-weight-black my-8">Plan du site</h1>
    <v-row>
      <v-col v-for="group in sitemapGroups" :key="group.title" cols="12" sm="6">
        <h2 class="my-2">{{ group.title }}</h2>
        <ul>
          <li v-for="link in group.links" :key="link.text">
            <router-link v-if="link.name" :to="{ name: link.name, params: link.params }">
              {{ (link.meta || {}).title || link.name }}
            </router-link>
            <a v-else :href="link.href">
              {{ (link.meta || {}).title }}
            </a>
          </li>
        </ul>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { routes } from "@/router"
import Constants from "@/constants"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "SiteMap",
  components: { BreadcrumbsNav },
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
    sitemapRoutes.push(
      ...keyMeasures.map((x) => ({
        name: "KeyMeasurePage",
        params: { id: x.id },
        meta: { title: x.shortTitle },
        sitemapGroup: Constants.SitemapGroups.LAW,
      }))
    )
    if (!isAuthenticated) {
      sitemapRoutes.push({
        href: "/creer-mon-compte",
        meta: { title: "Créer mon compte" },
        sitemapGroup: Constants.SitemapGroups.DIAG,
      })
      sitemapRoutes.push({
        href: "/s-identifier",
        meta: { title: "S'identifier" },
        sitemapGroup: Constants.SitemapGroups.DIAG,
      })
    }
    return {
      sitemapGroups: Object.values(Constants.SitemapGroups).map((g) => {
        return {
          title: g.label,
          links: sitemapRoutes.filter((f) => f.sitemapGroup?.label === g.label),
        }
      }),
    }
  },
}
</script>
