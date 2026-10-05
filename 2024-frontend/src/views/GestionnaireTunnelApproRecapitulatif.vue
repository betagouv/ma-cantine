<script setup>
import { computed, ref } from 'vue'
import { computedAsync } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import { useStoreCanteen } from '@/stores/canteen'
import { useStoreTeledeclaration } from '@/stores/teledeclaration'
import diagnosticServices from '@/services/diagnostics'
import canteenServices from '@/services/canteens'
import AppHelpCard from '@/components/AppHelpCard.vue'
import TunnelTeledeclarationAccordionsGroup from '@/components/TunnelTeledeclarationAccordionsGroup.vue'
import TunnelTeledeclarationModal from '@/components/TunnelTeledeclarationModal.vue'

/* Stores */
const canteenStore = useStoreCanteen()
const { canteenInformations } = storeToRefs(canteenStore)
const teledeclarationStore = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(teledeclarationStore)

/* TD CTA */
const canTeledeclare = computedAsync(async () => {
  const checkCanteen = await canteenServices.checkCanteen(canteenInformations.value.id)
  const checkDiagnostic = await diagnosticServices.checkDiagnostic(diagnostic.value.canteenId, diagnostic.value.id)
  return checkDiagnostic.isFilled && checkCanteen.isFilled
})
const sentence = computed(() => canTeledeclare.value ? "Je valide ma déclaration et la publication des données sur mon espace vitrine" : "Vous devez corriger votre télédéclaration pour la télédéclarer")
const icon = computed(() => canTeledeclare.value ? "fr-icon-checkbox-circle-fill fr-text-default--success" : "fr-icon-checkbox-line fr-text-mention--grey")
const isModalOpened = ref(false)
</script>
<template>
  <div>
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-2w">
      <div class="fr-col-12 fr-col-md-7">
        <h2 class="fr-h5">Votre télédéclaration vous semble t’elle cohérente ?</h2>
        <p v-if="canTeledeclare">Toutes vos données d’approvisionnement sont saisies, vous pouvez faire une relecture avant de soumettre votre télédéclaration.</p>
      </div>
      <div class="fr-col-12 fr-col-md-5">
        <AppHelpCard
          :title="sentence"
          :icon="icon"
          :changeIconColor="true"
        >
          <DsfrButton
            label="Télédéclarer"
            icon="ri-send-plane-line"
            :disabled="!canTeledeclare"
            @click="isModalOpened = true"
          />
        </AppHelpCard>
      </div>
    </div>
    <TunnelTeledeclarationAccordionsGroup />
    <TunnelTeledeclarationModal v-model:opened="isModalOpened" @close="isModalOpened = false" />
  </div>
</template>
