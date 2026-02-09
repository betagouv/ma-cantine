<script setup>
import { RouterView, useRoute } from "vue-router"
import { reactive, computed, watch } from "vue"
import AppHeader from "@/components/AppHeader.vue"
import AppBanner from "@/components/AppBanner.vue"
import AppBannerDemo from "@/components/AppBannerDemo.vue"
import AppFooter from "@/components/AppFooter.vue"
import AppBreadcrumb from "@/components/AppBreadcrumb.vue"
import NotificationCenter from "@/components/NotificationCenter.vue"

const layout = reactive({ fullscreen: false })
const routerViewClass = computed(() => (layout.fullscreen ? "" : "fr-container fr-mb-6w"))

const route = useRoute()
watch(route, (to) => {
  const suffix = "ma cantine"
  document.title = to.meta.title ? to.meta.title + " - " + suffix : suffix

  layout.fullscreen = to.meta.fullscreen
})
</script>

<template>
  <div>
    <AppHeader v-if="!layout.fullscreen" />
    <AppBannerDemo />
    <AppBanner v-if="!layout.fullscreen" />
    <DsfrNotice v-if="!layout.fullscreen" type="alert">
      Gestionnaires de crèches : rappel de laits infantiles, voir les lots concernés sur le site <a href="https://rappel.conso.gouv.fr/categorie/25" target="_blank">Rappel conso</a>
    </DsfrNotice>

    <main :class="routerViewClass">
      <AppBreadcrumb v-if="!layout.fullscreen" />
      <RouterView />
    </main>

    <AppFooter v-if="!layout.fullscreen" />

    <NotificationCenter />
  </div>
</template>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
fieldset {
  border: none;
}
.justify-space-between {
  justify-content: space-between;
}
</style>
