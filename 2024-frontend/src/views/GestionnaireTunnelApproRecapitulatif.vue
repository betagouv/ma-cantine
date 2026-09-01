<script setup>
import { computed } from 'vue'
import { computedAsync } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import { useStoreCanteen } from '@/stores/canteen'
import canteenService from '@/services/canteens'
import AppHelpCard from '@/components/AppHelpCard.vue'
import TunnelTeledeclarationAccordions from '@/components/TunnelTeledeclarationAccordions.vue'

/* Stores */
const canteenStore = useStoreCanteen()
const { canteenInformations } = storeToRefs(canteenStore)

/* Canteen action */
const lastYear = new Date().getFullYear() - 1
const canteenAction = computedAsync(async () => {
  const actions = await canteenService.fetchCanteensActions(lastYear)
  const currentCanteen = actions.find(canteen => canteen.id === canteenInformations.value.id)
  return currentCanteen.action
})

/* TD CTA */
const canTeledeclare = computed(() => canteenAction.value === "40_teledeclare")
const sentence = computed(() => canTeledeclare.value ? "Je valide ma déclaration et la publication des données sur mon espace vitrine" : "Vous devez corriger votre télédéclaration avant de déclarer")
const icon = computed(() => canTeledeclare.value ? "fr-icon-checkbox-circle-fill" : "fr-icon-checkbox-line")

const submitDeclaration = () => {
  console.log("submitDeclaration")
}
</script>
<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <h2 class="fr-h5">Votre télédéclaration vous semble t’elle cohérente ?</h2>
      <p>Toutes vos données d’approvisionnement sont saisies, vous pouvez faire une relecture avant de soumettre votre télédéclaration.</p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard
        :title="sentence"
        :icon="icon"
      >
        <DsfrButton
          label="Télédéclarer"
          icon="ri-send-plane-line"
          :disabled="!canTeledeclare"
          @click="submitDeclaration"
        />
      </AppHelpCard>
    </div>
  </div>
  <TunnelTeledeclarationAccordions />
</template>
