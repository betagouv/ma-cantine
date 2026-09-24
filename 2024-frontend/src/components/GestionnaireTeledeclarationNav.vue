<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import { storeToRefs } from "pinia"
import { useStoreCampaignDates } from "@/stores/campaignDates.js"

const props = defineProps(["canteen"])

/* Route */
const route = useRoute()
const teledeclarationEnCoursActive = computed(() => route.name === "GestionnaireCantineTeledeclarationEnCours")

/* Canteen */
const isGroupe = computed(() => props.canteen?.isGroupe)

/* Campaign dates */
const campaignDatesStore = useStoreCampaignDates()
const { currentCampaignInformations } = storeToRefs(campaignDatesStore)
const currentYear = window.TELEDECLARATION_YEAR
const isInTeledeclaration = computed(() => currentCampaignInformations.value.inTeledeclaration || false)
const isInCorrection = computed(() => currentCampaignInformations.value.inCorrection || false)
</script>

<template>
  <div
    v-if="isInTeledeclaration || isInCorrection"
    :class="{ 'fr-sidemenu__item--active': teledeclarationEnCoursActive }"
    class="gestionnaire-teledeclaration-nav fr-sidemenu__item"
  >
    <router-link :to="{ name: 'GestionnaireCantineTeledeclarationEnCours' }" class="fr-sidemenu__link">
      {{ isGroupe ? `Télédéclaration ${currentYear}` : `Ma télédéclaration ${currentYear}` }}
    </router-link>
  </div>
</template>

<style lang="scss">
.gestionnaire-teledeclaration-nav {
  [href] {
    background: none !important;
  }
}
</style>
