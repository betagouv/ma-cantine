<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"

const store = useRootStore()

const show = window.SHOW_BANNER
const publicBannerTitle = "La campagne de télédéclaration 2026 est prolongé jusqu'au 15 avril 2026."
const loggedBannerTitle = ""
const bannerTitle = computed(() => {
  return !!store.loggedUser && loggedBannerTitle ? loggedBannerTitle : publicBannerTitle
})
</script>

<template>
  <DsfrNotice v-if="show" :title="bannerTitle" type="info" />
</template>
