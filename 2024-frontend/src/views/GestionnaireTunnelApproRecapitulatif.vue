<script setup>
import { computed, ref } from 'vue'
import { computedAsync } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import { useStoreCanteen } from '@/stores/canteen'
import { useStoreDiagnostic } from '@/stores/diagnostic'
import diagnosticServices from '@/services/diagnostics'
import AppHelpCard from '@/components/AppHelpCard.vue'
import TunnelTeledeclarationAccordions from '@/components/TunnelTeledeclarationAccordions.vue'
import TunnelTeledeclarationErrors from '@/components/TunnelTeledeclarationErrors.vue'
import TunnelTeledeclarationModal from '@/components/TunnelTeledeclarationModal.vue'

/* Stores */
const canteenStore = useStoreCanteen()
const { canteenInformations } = storeToRefs(canteenStore)
const diagnosticStore = useStoreDiagnostic()
const { diagnosticCurrentCampaign } = storeToRefs(diagnosticStore)

/* TD CTA */
const canTeledeclare = computedAsync(async () => {
  const check = await diagnosticServices.checkDiagnostic(canteenInformations.value.id, diagnosticCurrentCampaign.value.id)
  return check.isFilled
})
const sentence = computed(() => canTeledeclare.value ? "Je valide ma déclaration et la publication des données sur mon espace vitrine" : "Vous devez corriger votre télédéclaration avant de déclarer")
const icon = computed(() => canTeledeclare.value ? "fr-icon-checkbox-circle-fill" : "fr-icon-checkbox-line")
const isModalOpened = ref(false)
</script>
<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-2w">
    <div class="fr-col-12 fr-col-md-7">
      <h2 class="fr-h5">Votre télédéclaration vous semble t’elle cohérente ?</h2>
      <p>Toutes vos données d’approvisionnement sont saisies, vous pouvez faire une relecture avant de soumettre votre télédéclaration.</p>
      <TunnelTeledeclarationErrors />
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
          @click="isModalOpened = true"
        />
      </AppHelpCard>
    </div>
  </div>
  <TunnelTeledeclarationAccordions />
  <TunnelTeledeclarationModal v-model:opened="isModalOpened" @close="isModalOpened = false" />
</template>
