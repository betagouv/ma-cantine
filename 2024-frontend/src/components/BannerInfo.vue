<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"

const store = useRootStore()

const show = window.SHOW_BANNER
const publicBannerTitle = "Campagne de télédéclaration du 12 au 31 mars 2026. Une prolongation de quelques jours est prévue - précisions le 31 mars."
const loggedBannerTitle = "Campagne de télédéclaration 2026 : du 12 janvier au 31 mars 2026. Prolongation : télédéclarations possibles jusqu'à la campagne de correction - précisions le 31 mars."
const bannerTitle = computed(() => {
  return !!store.loggedUser && loggedBannerTitle ? loggedBannerTitle : publicBannerTitle
})
</script>

<template>
  <DsfrNotice v-if="show" :title="bannerTitle" type="info" />
</template>
