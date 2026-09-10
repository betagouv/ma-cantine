<script setup>
import { computed, ref } from 'vue'
import { computedAsync } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useStoreCanteen } from '@/stores/canteen'
import { useStoreDiagnostic } from '@/stores/diagnostic'
import diagnosticServices from '@/services/diagnostics'
import AppHelpCard from '@/components/AppHelpCard.vue'
import TunnelTeledeclarationAccordions from '@/components/TunnelTeledeclarationAccordions.vue'
import TunnelTeledeclarationErrors from '@/components/TunnelTeledeclarationErrors.vue'
import TunnelTeledeclarationModal from '@/components/TunnelTeledeclarationModal.vue'

/* Router */
const router = useRouter()

/* Stores */
const canteenStore = useStoreCanteen()
const { canteenInformations } = storeToRefs(canteenStore)
const diagnosticStore = useStoreDiagnostic()
const { diagnosticCurrentCampaign } = storeToRefs(diagnosticStore)

/* TD CTA */
const canTeledeclare = computedAsync(async () => {
  const check = await diagnosticServices.checkDiagnostic(diagnosticCurrentCampaign.value.canteenId, diagnosticCurrentCampaign.value.id)
  return check.isFilled
})
const sentence = computed(() => canTeledeclare.value ? "Je valide ma déclaration et la publication des données sur mon espace vitrine" : "Vous devez corriger votre télédéclaration avant de déclarer")
const icon = computed(() => canTeledeclare.value ? "fr-icon-checkbox-circle-fill" : "fr-icon-checkbox-line")
const isModalOpened = ref(false)

/* Redirects */
const buttons = computed(() => {
  const buttonsGroup = []
  if (!canteenInformations.value.isGroupe) {
    buttonsGroup.push({
      label: 'Voir ma page publique',
      secondary: true,
      icon: 'ri-global-line',
      onclick: () => {
        router.push({ name: 'GestionnaireCantinePagePublique' })
      },
    })
  }
  buttonsGroup.push({
    label: 'Compléter les volets thématiques',
    icon: 'ri-arrow-right-line',
    iconRight: true,
    onclick: () => {
      router.push({ name: 'GestionnaireTunnelVoletsThematiques' })
    },
  })
  return buttonsGroup
})

</script>
<template>
  <div v-if="diagnosticCurrentCampaign.isTeledeclared">
    <DsfrAlert
      title="Votre télédéclaration a été prise en compte"
      description="Vous pouvez retrouver votre justificatif de déclaration et la synthèse de votre qualité de produits dans votre espace cantine."
      icon="ri-checkbox-circle-fill"
      type="success"
      class="fr-mb-4w"
    />
    <h2 class="fr-h5">Compléter les volets thématiques et votre page publique</h2>
    <p class="ma-cantine--bold">Envie de faire rayonner vos engagements pour une restauration collective durable et de qualité ?</p>
    <p>
      Renseignez vos avancées sur <span class="ma-cantine--bold">l’information des convives</span>, la <span class="ma-cantine--bold">lutte contre le gaspillage alimentaire</span>, la <span class="ma-cantine--bold">diversification des sources de protéines</span> et <span class="ma-cantine--bold">menus végétariens</span> et la <span class="ma-cantine--bold">substitution des plastiques</span>, pour :
    </p>
    <ul class="fr-mb-4w">
      <li>
        <span class="ma-cantine--bold">Rendre visible votre prise en compte des objectifs de la loi EGalim</span> via votre page publique (moteur de recherche “Trouver une cantine”)
      </li>
      <li>
        <span class="ma-cantine--bold">Contribuer de manière anonyme à l’Observatoire EGalim</span> en restauration collective et au bilan statistique annuel, transmis chaque année au Parlement.
      </li>
    </ul>
    <DsfrButtonGroup :buttons="buttons" inlineLayoutWhen="always" align="right" />
  </div>
  <div v-else>
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
  </div>
</template>
