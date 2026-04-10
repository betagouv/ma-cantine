<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import documentation from "@/data/documentation.json"

const store = useRootStore()

const show = window.SHOW_BANNER
const publicBannerTitle = "DROIT À L’ERREUR : du 16 au 29 avril 2026."
const loggedBannerTitle = ""
const bannerTitle = computed(() => {
  return !!store.loggedUser && loggedBannerTitle ? loggedBannerTitle : publicBannerTitle
})
</script>

<template>
  <DsfrNotice v-if="show" type="info" :title="bannerTitle">
    <template #desc>
      Valable uniquement pour les établissements qui ont validé leur télédéclaration dans les temps. Depuis votre bilan, vous pouvez corriger vos informations si besoin
      <a :href="documentation.correctionCampaign" target="_blank">voir l’article d’aide pour en savoir plus</a>.
    </template>
  </DsfrNotice>
</template>
