<script setup>
import { RouterView } from "vue-router"
import { ref } from "vue"

const logoText = ["Ministère", "de l’Agriculture", "et de la Souveraineté", "Alimentaire"]
const serviceTitle = "ma cantine"
const placeholder = ""
const homeTo = "/"
const quickLinks = [
  { label: "Se connecter", to: "/login", class: "fr-icon-user-fill" },
  {
    label: "S’enregistrer",
    to: "/signup",
    icon: "ri-account-circle-line",
  },
]

const nb = ref(0)
const handleClick = () => {
  nb.value++
}
</script>

<template>
  <div style="position: relative; padding-bottom: 4rem;">
    <DsfrHeader :logo-text :service-title :placeholder :home-to :quick-links />
    <div class="fr-container fr-my-2w">
      <div class="fr-grid-row">
        <img src="/static/images/badges/appro.svg" width="125" height="125" />
      </div>
      <div class="fr-grid-row">
        <!-- example of loading from web/static -->
        <DsfrButton size="lg" icon="fr-icon-home-4-fill" label="Accueil" @click="handleClick()" />
      </div>
      <div class="fr-grid-row">
        <p>Cliqué {{ nb }} fois</p>
      </div>
    </div>

    <main class="fr-container fr-pb-2w">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
