<template>
  <div class="text-left">
    <h1 class="font-weight-black my-8">Plan du site</h1>
    <v-row>
      <v-col v-for="group in mapGroups" :key="group.title" cols="6">
        <h2 class="my-2">{{ group.title }}</h2>
        <ul>
          <li v-for="link in group.links.filter((l) => !l.props)" :key="link.text">
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
    let mcRoutes = JSON.parse(JSON.stringify(routes))
    mcRoutes.forEach((r) => {
      if (r.children) {
        mcRoutes.push(...r.children)
      }
    })
    return {
      mapGroups: [
        {
          title: "S'informer sur les lois",
          links: mcRoutes.filter((f) => f.mcGroup === "LAW"),
        },
        {
          title: "Se diagnostiquer",
          links: mcRoutes.filter((f) => f.mcGroup === "DIAG"),
        },
        {
          title: "Améliorer votre offre",
          links: mcRoutes.filter((f) => f.mcGroup === "ACTION"),
        },
        {
          title: "Informations sur le site",
          links: mcRoutes.filter((f) => f.mcGroup === "SITE"),
        },
      ],
    }
  },
}
</script>
