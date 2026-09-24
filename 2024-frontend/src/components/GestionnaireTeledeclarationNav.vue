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
</script>
<template>
  <div
    v-if="isInTeledeclaration || isInCorrection"
    :class="{ 'fr-sidemenu__item--active': teledeclarationEnCoursActive }"
    class="gestionnaire-teledeclaration-nav fr-sidemenu__item"
  >
    <router-link :to="{ name: 'GestionnaireCantineTeledeclarationEnCours' }" class="gestionnaire-teledeclaration-nav__bloc fr-sidemenu__link">
      <DsfrBadge :label="diagnosticBadge.label" :type="diagnosticBadge.type" />
      {{ isGroupe ? `Télédéclaration ${currentYear}` : `Ma télédéclaration ${currentYear}` }}
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
}
</style>
