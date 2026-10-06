<script setup>
import { computed } from "vue"
import { computedAsync } from "@vueuse/core"
import { useRoute } from "vue-router"
import { storeToRefs } from "pinia"
import { useStoreCampaignDates } from "@/stores/campaignDates.js"
import canteensService from "@/services/canteens.js"
import AppBadgeDiagnostic from "@/components/AppBadgeDiagnostic.vue"
import IconMacaronAppro from "@/components/IconMacaronAppro.vue"
import IconMacaronInfo from "@/components/IconMacaronInfo.vue"
import IconMacaronWaste from "@/components/IconMacaronWaste.vue"
import IconMacaronDiversification from "@/components/IconMacaronDiversification.vue"
import IconMacaronPlastic from "@/components/IconMacaronPlastic.vue"

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

/* Check */
// TODO : make it dynamic with the check
const approIconAlt = computed(() => 'Volet approvisionnement non complété')
const infoIconAlt = computed(() => 'Volet information convive non complété')
const wasteIconAlt = computed(() => 'Volet gestion du gaspillage alimentaire non complété')
const diversificationIconAlt = computed(() => 'Volet diversification des protéines non complété')
const plasticIconAlt = computed(() => 'Volet réductions du plastique non complété')
</script>
<template>
  <div v-if="isInTeledeclaration || isInCorrection" class="gestionnaire-teledeclaration-nav fr-sidemenu">
    <div class="fr-sidemenu__inner">
      <ul class="fr-sidemenu__list">
        <li :class="{ 'fr-sidemenu__item--active': teledeclarationEnCoursActive }" class="fr-sidemenu__item">
          <router-link :to="{ name: 'GestionnaireCantineTeledeclarationEnCours' }" class="gestionnaire-teledeclaration-nav__bloc fr-sidemenu__link">
            <AppBadgeDiagnostic :action="currentCanteenAction" />
            <span>{{ isGroupe ? `Télédéclaration ${currentYear}` : `Ma télédéclaration ${currentYear}` }}</span>
            <span class="gestionnaire-teledeclaration-nav__macarons-container">
              <IconMacaronAppro :label="approIconAlt" status="empty" />
              <IconMacaronInfo :label="infoIconAlt" status="empty" />
              <IconMacaronWaste :label="wasteIconAlt" status="empty" />
              <IconMacaronDiversification :label="diversificationIconAlt" status="empty" />
              <IconMacaronPlastic :label="plasticIconAlt" status="empty" />
            </span>
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<style lang="scss">
.gestionnaire-teledeclaration-nav {
  [href] {
    background-image: none !important;
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

    svg {
      flex: 1 1 0;
      min-width: 0;
      width: 100%;
      height: auto;
    }
  }
}
</style>
