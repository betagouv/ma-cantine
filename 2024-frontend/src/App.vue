<script setup>
import { RouterView, useRoute } from "vue-router"
import { reactive, computed, watch } from "vue"
import NotificationSnackbar from "@/components/NotificationSnackbar.vue"

import { useRootStore } from "@/stores/root"
const store = useRootStore()

const logoText = ["Ministère", "de l’Agriculture", "et de la Souveraineté", "Alimentaire"]
const serviceTitle = "ma cantine"

const layout = reactive({ fullscreen: false })
const routerViewClass = computed(() => (layout.fullscreen ? "" : "fr-container fr-pb-2w"))

const route = useRoute()
watch(route, (to) => {
  const suffix = "ma cantine"
  document.title = to.meta.title ? to.meta.title + " - " + suffix : suffix

  layout.fullscreen = to.meta.fullscreen
})

const notifications = computed(() => store.notifications)
</script>

<template>
  <div>
    <DsfrHeader v-if="!layout.fullscreen" :logo-text :service-title />

    <main :class="routerViewClass">
      <RouterView />
    </main>

    <DsfrFooter v-if="!layout.fullscreen" />

    <div id="notification-center" class="fr-col-12 fr-col-sm-8 fr-col-md-6 fr-col-lg-4">
      <NotificationSnackbar v-for="notification in notifications" :key="notification.id" :notification="notification" />
    </div>
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
#notification-center {
  position: fixed;
  z-index: 1000;
  height: fit-content;
  right: 0;
  top: 0;
}
</style>
