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

</script>

<template>
  <h1>{{ route.meta.title }}</h1>
  <div class="fr-grid-row">
    <section v-for="section in sections" :key="section.title" class="fr-col-6">
      <h2>{{ section.title }}</h2>
      <ul>
        <li v-for="page in section.pages">
          <AppLinkRouter :title="page.title" :to="page" />
        </li>
      </ul>
    </section>
  </div>
</template>
