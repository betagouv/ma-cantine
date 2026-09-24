<script setup>
import { computed } from "vue"
import { computedAsync } from "@vueuse/core"
import { useRoute } from "vue-router"
import { storeToRefs } from "pinia"
import { useStoreCampaignDates } from "@/stores/campaignDates.js"
import diagnosticsBadgeService from "@/services/diagnosticsBadge.js"
import canteensService from "@/services/canteens.js"

const props = defineProps(["canteen"])
const route = useRoute()
const teledeclarationEnCoursActive = computed(() => route.name === "GestionnaireCantineTeledeclarationEnCours")

/* Campaign dates */
const campaignDatesStore = useStoreCampaignDates()
const { currentCampaignInformations } = storeToRefs(campaignDatesStore)
const currentYear = window.TELEDECLARATION_YEAR
const isInTeledeclaration = computed(() => currentCampaignInformations.value.inTeledeclaration || false)
const isInCorrection = computed(() => currentCampaignInformations.value.inCorrection || false)

/* Canteen */
const tdYear = window.TELEDECLARATION_YEAR
const isGroupe = computed(() => props.canteen?.isGroupe)
const allCanteens = computedAsync(async () => await canteensService.fetchCanteensActions(tdYear), [])
const currentCanteenAction = computed(() => {
  if (!allCanteens.value) return null
  const canteen = allCanteens.value.find((canteen) => canteen.id === props.canteen.id)
  return canteen?.action || null
})
const diagnosticBadge = computed(() => diagnosticsBadgeService.getBadge(currentCanteenAction.value, currentCampaignInformations.value))

/* Check */
// TODO : make it dynamic with the check
const approIconLink = computed(() => '/static/images/badges/badge-appro-disabled.svg')
const infoIconLink = computed(() => '/static/images/badges/badge-info-disabled.svg')
const wasteIconLink = computed(() => '/static/images/badges/badge-waste-disabled.svg')
const diversificationIconLink = computed(() => '/static/images/badges/badge-diversification-disabled.svg')
const plasticIconLink = computed(() => '/static/images/badges/badge-plastic-disabled.svg')
const approIconAlt = computed(() => 'Volet approvisionnement non complété')
const infoIconAlt = computed(() => 'Volet information convive non complété')
const wasteIconAlt = computed(() => 'Volet gestion du gaspillage alimentaire non complété')
const diversificationIconAlt = computed(() => 'Volet diversification des protéines non complété')
const plasticIconAlt = computed(() => 'Volet réductions du plastique non complété')
</script>
<template>
  <div
    v-if="isInTeledeclaration || isInCorrection"
    :class="{ 'fr-sidemenu__item--active': teledeclarationEnCoursActive }"
    class="gestionnaire-teledeclaration-nav fr-sidemenu__item"
  >
    <router-link :to="{ name: 'GestionnaireCantineTeledeclarationEnCours' }" class="gestionnaire-teledeclaration-nav__bloc fr-sidemenu__link">
      <DsfrBadge :label="diagnosticBadge.label" :type="diagnosticBadge.type" />
      <span>{{ isGroupe ? `Télédéclaration ${currentYear}` : `Ma télédéclaration ${currentYear}` }}</span>
      <span class="gestionnaire-teledeclaration-nav__macarons-container">
        <img :src="approIconLink" :alt="approIconAlt">
        <img :src="infoIconLink" :alt="infoIconAlt">
        <img :src="wasteIconLink" :alt="wasteIconAlt">
        <img :src="diversificationIconLink" :alt="diversificationIconAlt">
        <img :src="plasticIconLink" :alt="plasticIconAlt">
      </span>
    </router-link>
  </div>
</template>

<style lang="scss">
.gestionnaire-teledeclaration-nav {
  [href] {
    background: none !important;
  }

  &__bloc {
    display: flex;
    flex-direction: column !important;
    align-items: flex-start !important;
    gap: 0.5rem;
  }

  &__macarons-container {
    display: flex;
    gap: 0.5rem;
    border: 1px solid var(--border-disabled-grey);
    border-radius: 0.5rem;
    padding: 0.5rem;
    width: 70%;

    img {
      flex: 1 1 0;
      min-width: 0;
      width: 100%;
      height: auto;
    }
  }
}
</style>
