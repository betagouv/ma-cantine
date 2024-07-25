<script setup>
import { RouterView, useRoute } from "vue-router"
import { reactive, computed, watch } from "vue"

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
</script>

<template>
  <div>
    <DsfrHeader v-if="!layout.fullscreen" :logo-text :service-title />

    <main :class="routerViewClass">
      <RouterView />
    </main>

    <DsfrFooter v-if="!layout.fullscreen" />
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
</style>
