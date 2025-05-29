<script setup>
import { useRoute } from "vue-router"
import { sectionId } from "@/constants/site-map.js"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import keyMeasures from "@/data/key-measures.json"
import vue2routes from "@/router/vue2.js"
import vue3routes from "@/router/vue3.js"

/* Setup */
const route = useRoute()

/* Generate section's content */
const sections = []

const routeInSection = (route, sectionName) => {
  return route.meta ? route.meta.siteMap === sectionName : false
}

const lawContent = () => {
  const lawVue2Pages = vue2routes.filter((route) => routeInSection(route, sectionId.law))
  const lawVue3Pages = vue3routes.filter((route) => routeInSection(route, sectionId.law))
  const keyMeasuresPages = keyMeasures.map((x) => ({
    name: "KeyMeasurePage",
    params: { id: x.id },
    meta: {
      title: x.title,
    },
  }))

  return {
    title: "S'informer sur les lois",
    pages: [...lawVue2Pages, ...lawVue3Pages, ...keyMeasuresPages],
  }
}

const diagContent = () => {
  const diagVue2Pages = vue2routes.filter((route) => routeInSection(route, sectionId.diag))
  const diagVue3Pages = vue3routes.filter((route) => routeInSection(route, sectionId.diag))

  return {
    title: "Se diagnostiquer",
    pages: [...diagVue2Pages, ...diagVue3Pages],
  }
}

const actionContent = () => {
  const actionVue2Pages = vue2routes.filter((route) => routeInSection(route, sectionId.action))
  const actionVue3Pages = vue3routes.filter((route) => routeInSection(route, sectionId.action))

  return {
    title: "Améliorer votre offre",
    pages: [...actionVue2Pages, ...actionVue3Pages],
  }
}

const siteContent = () => {
  const siteVue2Pages = vue2routes.filter((route) => routeInSection(route, sectionId.site))
  const siteVue3Pages = vue3routes.filter((route) => routeInSection(route, sectionId.site))

  return {
    title: "Informations sur le site",
    pages: [...siteVue2Pages, ...siteVue3Pages],
  }
}

sections.push(lawContent())
sections.push(diagContent())
sections.push(actionContent())
sections.push(siteContent())
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
