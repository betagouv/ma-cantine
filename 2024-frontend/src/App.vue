<script setup>
import { RouterView, useRoute } from "vue-router"
import { computed, watch } from "vue"
import AppHeader from "@/components/AppHeader.vue"
import AppFooter from "@/components/AppFooter.vue"
import AppBreadcrumb from "@/components/AppBreadcrumb.vue"
import AppBanners from "@/components/AppBanners.vue"
import NotificationCenter from "@/components/NotificationCenter.vue"

const route = useRoute()
const isFullscreen = computed(() => route.meta.fullscreen)
const isTunnel = computed(() => route.meta.isTunnel)

watch(route, (to) => {
  const suffix = "ma cantine"
  document.title = to.meta.title ? to.meta?.title + " - " + suffix : suffix
})
</script>

<template>
  <AppHeader v-if="!isFullscreen" :show-nav="!isTunnel" />
  <AppBanners v-if="!isFullscreen && !isTunnel" />

  <main :class="{ 'fr-container fr-mb-6w': !isFullscreen }">
    <AppBreadcrumb v-if="!isFullscreen && !isTunnel" />
    <RouterView />
  </main>

  <AppFooter v-if="!isFullscreen" />

  <NotificationCenter />
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
