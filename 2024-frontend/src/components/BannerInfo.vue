<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"

const store = useRootStore()

const show = window.SHOW_BANNER
const publicBannerTitle = "La campagne de télédéclaration 2026 est prolongée jusqu'au 15 avril 2026"
const loggedBannerTitle = ""
const bannerTitle = computed(() => {
  return !!store.loggedUser && loggedBannerTitle ? loggedBannerTitle : publicBannerTitle
})
const bannerLink = "https://agriculture.gouv.fr/exemplarite-de-letat-dans-la-restauration-collective-annie-genevard-et-david-amiel-mobilisent-les"
</script>

<template>
  <DsfrNotice v-if="show" type="info">
    {{ bannerTitle }} : <a :href="bannerLink" target="_blank">voir le communiqué de presse</a>.
  </DsfrNotice>
</template>
