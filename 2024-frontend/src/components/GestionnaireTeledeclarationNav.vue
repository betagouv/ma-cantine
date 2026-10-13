<script setup>
import { computed } from "vue"
import { computedAsync } from "@vueuse/core"
import { useRoute } from "vue-router"
import { storeToRefs } from "pinia"
import { useStoreCampaignDates } from "@/stores/campaignDates.js"
import { useStoreTeledeclaration } from "@/stores/teledeclaration.js"
import canteensService from "@/services/canteens.js"
import AppBadgeDiagnostic from "@/components/AppBadgeDiagnostic.vue"
import AppSeparator from "@/components/AppSeparator.vue"
import IconLink from "@/components/IconLink.vue"
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

/* Macaron status */
const teledeclarationStore = useStoreTeledeclaration()
const { diagnoticCheck, isTeledeclared } = storeToRefs(teledeclarationStore)
const getStatus = (name) => {
  if (name !== "appro") return "empty"
  if (isTeledeclared.value) return "teledeclared"
  if (diagnoticCheck.value.isClean) return "fill"
  return "empty"
}
</script>
<template>
  <div v-if="isInTeledeclaration || isInCorrection" class="gestionnaire-teledeclaration-nav fr-sidemenu">
    <div class="fr-sidemenu__inner">
      <ul class="fr-sidemenu__list">
        <li :class="{ 'fr-sidemenu__item--active': teledeclarationEnCoursActive }" class="fr-sidemenu__item">
          <router-link :to="{ name: 'GestionnaireCantineTeledeclarationEnCours' }" class="gestionnaire-teledeclaration-nav__bloc fr-sidemenu__link">
            <AppBadgeDiagnostic :action="currentCanteenAction" />
            <span>{{ isGroupe ? `Télédéclaration ${currentYear}` : `Ma télédéclaration ${currentYear}` }}</span>
            <div class="gestionnaire-teledeclaration-nav__indicator ma-cantine--width-100">
              <IconLink bottom="50%" class="gestionnaire-teledeclaration-nav__link" />
              <div class="gestionnaire-teledeclaration-nav__macarons fr-py-1v fr-px-1w">
                <IconMacaronAppro :status="getStatus('appro')" />
                <AppSeparator orientation="vertical" class="fr-my-0-5v" />
                <IconMacaronInfo :status="getStatus('info')" />
                <IconMacaronWaste :status="getStatus('waste')" />
                <IconMacaronDiversification :status="getStatus('diversification')" />
                <IconMacaronPlastic :status="getStatus('plastic')" />
              </div>
            </div>
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

  &__indicator {
    display: flex;
  }

  &__link {
    flex: 0 0 0.5rem;
  }

  &__macarons {
    flex: 0 0 auto;
    display: flex;
    align-items: stretch;
    gap: 0.75rem;
    border: 1px solid var(--border-default-grey);
    border-radius: 0.5rem;

    svg {
      flex: 0 0 1.375rem;
      width: 1.375rem;
      height: 1.375rem;
    }
  }
}
</style>
