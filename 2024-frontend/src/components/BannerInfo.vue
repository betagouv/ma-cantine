<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import documentation from "@/data/documentation.json"

const store = useRootStore()

const show = window.SHOW_BANNER
const publicBannerTitle = "La réglementation évolue."
const loggedBannerTitle = ""
const bannerTitle = computed(() => {
  return !!store.loggedUser && loggedBannerTitle ? loggedBannerTitle : publicBannerTitle
})
</script>

<template>
  <DsfrNotice v-if="show" type="info" :title="bannerTitle">
    <template #desc>
      La loi d’urgence pour la protection et la souveraineté agricoles, publiée le 19 août 2026, introduit de nouvelles dispositions. Elle modifie également certaines mesures relatives aux approvisionnements et fait évoluer les modalités de télédéclaration. La documentation <em>ma cantine</em> est progressivement mise à jour pour intégrer ces changements. Plus d'informations sur
      <a :href="documentation.loiUPSA" target="_blank">notre centre documentaire</a>.
    </template>
  </DsfrNotice>
</template>
