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

const lawContent = () => {
  const lawVue2Pages = vue2routes.filter((route) => (route.meta ? route.meta.siteMap === sectionId.law : false))
  const lawVue3Pages = vue3routes.filter((route) => (route.meta ? route.meta.siteMap === sectionId.law : false))
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
  const diagVue2Pages = vue2routes.filter((route) => (route.meta ? route.meta.siteMap === sectionId.diag : false))
  const diagVue3Pages = vue3routes.filter((route) => (route.meta ? route.meta.siteMap === sectionId.diag : false))

  return {
    title: "Se diagnostiquer",
    pages: [...diagVue2Pages, ...diagVue3Pages],
  }
}

sections.push(lawContent())
sections.push(diagContent())
</script>

<template>
  <h1>{{ route.meta.title }}</h1>
  <div class="fr-grid-row">
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
