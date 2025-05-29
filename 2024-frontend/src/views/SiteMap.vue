<script setup>
import { useRootStore } from "@/stores/root"
import { useRoute } from "vue-router"
import { sectionId } from "@/constants/site-map.js"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import keyMeasures from "@/data/key-measures.json"
import vue2routes from "@/router/vue2.js"
import vue3routes from "@/router/vue3.js"

/* Setup */
const route = useRoute()
const store = useRootStore()

/* Pages not present in the router */
const keyMeasuresPages = keyMeasures.map((x) => ({
  name: "KeyMeasurePage",
  params: { id: x.id },
  meta: { title: x.title },
}))

const loginPages = [
  {
    path: "/creer-mon-compte",
    meta: { title: "Créer mon compte" },
  },
  {
    path: "/s-identifier",
    meta: { title: "S'identifier" },
  },
]

/* Get pages from vue2 and vue3 routers */
const routeIsInSection = (route, sectionName) => {
  return route?.meta?.siteMap === sectionName
}

const canUserAccessPage = (route) => {
  if (route?.meta?.authenticationRequired && !store.loggedUser) return false
  return true
}

const getPages = (sectionId) => {
  const vue2pages = vue2routes.filter((route) => routeIsInSection(route, sectionId) && canUserAccessPage(route))
  const vue3pages = vue3routes.filter((route) => routeIsInSection(route, sectionId) && canUserAccessPage(route))

  return [...vue2pages, ...vue3pages]
}

/* Generate section's content */
const sections = [
  {
    title: "S'informer sur les lois",
    pages: [...getPages(sectionId.law), ...keyMeasuresPages],
  },
  {
    title: "Se diagnostiquer",
    pages: store.loggedUser ? getPages(sectionId.diag) : [...getPages(sectionId.diag), ...loginPages],
  },
  {
    title: "Améliorer votre offre",
    pages: getPages(sectionId.action),
  },
  {
    title: "Informations sur le site",
    pages: getPages(sectionId.site),
  },
]
</script>

<template>
  <h1>{{ route.meta.title }}</h1>
  <div class="fr-grid-row fr-grid-row--gutters">
    <section v-for="section in sections" :key="section.title" class="fr-col-6">
      <h2>{{ section.title }}</h2>
      <ul>
        <li v-for="page in section.pages" :key="page.name">
          <AppLinkRouter :title="page.meta.title" :to="page" />
        </li>
      </ul>
    </section>
  </div>
</template>
