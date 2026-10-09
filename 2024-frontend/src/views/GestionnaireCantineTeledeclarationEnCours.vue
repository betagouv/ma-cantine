<script setup>
import { computed, ref } from "vue"
import { computedAsync } from "@vueuse/core"
import { storeToRefs } from "pinia"
import { useRouter } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen.js"
import { useStoreTeledeclaration } from "@/stores/teledeclaration.js"
import { useRootStore } from "@/stores/root.js"
import diagnosticService from "@/services/diagnostics.js"
import documentation from "@/data/documentation.json"
import GestionnaireSidebarTitle from "@/components/GestionnaireSidebarTitle.vue"
import AppHelpCard from "@/components/AppHelpCard.vue"
import DiagnosticSatellitesLinked from "@/components/DiagnosticSatellitesLinked.vue"
import DiagnosticPurchasesLinked from "@/components/DiagnosticPurchasesLinked.vue"
import DiagnosticSummary from "@/components/DiagnosticSummary.vue"
import DiagnosticPdf from "@/components/DiagnosticPdf.vue"
import DiagnosticModalCancel from "@/components/DiagnosticModalCancel.vue"

const rootStore = useRootStore()
const canteenStore = useStoreCanteen()
const router = useRouter()
const currentYear = new Date().getFullYear()
const { canteenInformations } = storeToRefs(canteenStore)

/* Teledeclaration */
const teledeclarationStore = useStoreTeledeclaration()
const { hasDiagnostic, canteenAction, isTeledeclared } = storeToRefs(teledeclarationStore)
const year = teledeclarationStore.getYear()
const canTeledeclare = computed(() => canteenAction.value === "40_teledeclare")
const diagnosticRecap = computedAsync(async () => {
  if (!isTeledeclared.value) return null
  const diagnostics = await diagnosticService.fetchDiagnosticsRecap(canteenInformations.value.id)
  return diagnostics.find((diagnostic) => diagnostic.year === year) || null
}, null)

/* Content */
const pageTitle = computed(() => canteenInformations.value.isGroupe ? `Télédéclaration ${currentYear}` : `Ma télédéclaration ${currentYear}`)
const buttonTop = computed(() => {
  switch (true) {
    case isTeledeclared.value:
      return { label: 'Modifier ma télédéclaration', icon: 'fr-icon-edit-line', openModal: true }
    case canTeledeclare.value:
      return { label: 'Valider ma télédéclaration', icon: 'ri-send-plane-line', pageName: "GestionnaireTunnelApproRecapitulatif" }
    case hasDiagnostic.value:
      return { label: 'Reprendre ma télédéclaration', icon: 'ri-send-plane-line', pageName: "GestionnaireTunnelApproInformations" }
    default:
      return { label: 'Faire ma télédéclaration', icon: 'ri-send-plane-line' }
  }
})

/* Navigation */
const showCancelModal = ref(false)
const onClickButtonTop = () => {
  if (buttonTop.value.openModal) showCancelModal.value = true
  else openTunnel(buttonTop.value.pageName)
}

const openTunnel = (pageName) => {
  if (!pageName) createDiagnostic()
  else goToTunnel(pageName)
}

const createDiagnostic = () => {
  diagnosticService.createDiagnostic(canteenInformations.value.id, { year })
    .then((response) => {
      if(response.status === "error") showError(response.message)
      else {
        teledeclarationStore.setDiagnostic(response)
        goToTunnel("GestionnaireTunnelApproInformations")
      }
    })
    .catch((error) => showError(error.message))
}
const goToTunnel = (pageName) => router.push({ name: pageName })
const showError = (message) => rootStore.notifyServerError(message)
</script>
<template>
  <DsfrAlert class="fr-mb-4w" title="Nouvelle télédéclaration en cours de développement" description="Dans le cadre d'amélioration de la télédéclaration 2027, cette page est en cours de développement et n'est pas encore complète ou stabilisée. Vous pouvez toutefois déjà commencer à l'utiliser mais il est possible que vous rencontriez des bugs ou des fonctionnalités non disponibles." type="warning" />
  <GestionnaireSidebarTitle :title="pageTitle">
    <DsfrButton
      v-if="buttonTop"
      primary
      @click="onClickButtonTop"
      :label="buttonTop.label"
      :icon="buttonTop.icon"
    />
  </GestionnaireSidebarTitle>
  <DiagnosticModalCancel :opened="showCancelModal" @close="showCancelModal = false" />

  <DsfrAlert v-if="canTeledeclare" class="fr-mb-5w" title="Il reste une étape pour finaliser votre télédéclaration." description="Vos données sont complètes il ne reste qu’à télédéclarer pour qu’elles soient prise en compte." type="info" />
  <div class="fr-mb-5w fr-grid-row fr-grid-row--gutters fr-grid-row--top">
    <div v-if="isTeledeclared" class="fr-col-12 fr-col-md-7">
      <h3 class="fr-h5 fr-mb-4w">Valorisez et partagez vos résultats.</h3>
      <p>
        Retrouvez et partagez vos résultats sur votre page publique pour valoriser vos initiatives auprès de votre collectivité, de vos convives et de l'ensemble des acteurs de votre territoire.
      </p>
    </div>
    <div v-else class="fr-col-12 fr-col-md-7">
      <h3 class="fr-h5 fr-mb-4w">Réalisez le bilan de l’année précédente sur les différents volets de la loi EGalim.</h3>
      <p v-if="canteenInformations.isGroupe">
        Vous allez télédéclarer de manière mutualisée au sein d’une même entité de gestion. Les montants d’achats seront répartis automatiquement au prorata du nombre de couverts annuels de chaque cantine du groupe.
        <strong>Les gestionnaires des cantines n’auront pas accès aux montants d’achats, mais uniquement aux résultats (en %).</strong>
      </p>
      <p v-else>
        La télédéclaration comporte 2 principales étapes : le volet approvisionnements (simplifiés ou détaillés) et les volets thématiques (facultatifs).
      </p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard v-if="isTeledeclared" title="Les documents essentiels :" :no-icon="true">
        <DiagnosticPdf v-if="diagnosticRecap" :diagnostic="diagnosticRecap" :canteen-id="canteenInformations.id" />
      </AppHelpCard>
      <AppHelpCard v-else title="Infos utiles pour consolider vos données">
        <ul class="ma-cantine--unstyled-list fr-mb-0">
          <li class="fr-mb-1w">
            <a :href="documentation.teledeclarationMatrice" target="_blank">La matrice de télédéclaration</a>
          </li>
          <li class="fr-mb-1w">
            <a :href="documentation.teledeclarationChecklist" target="_blank">L’antisèche</a>
          </li>
          <li class="fr-mb-1w">
            <a :href="documentation.gestionConcedee" target="_blank">Gestion concédée : bien m’organiser</a>
          </li>
        </ul>
      </AppHelpCard>
    </div>
  </div>
  <DiagnosticSummary class="fr-mb-5w" />
  <div v-if="!canTeledeclare && !isTeledeclared">
    <h3 class="fr-h5 fr-mb-4w">Avant de débuter :</h3>
    <DiagnosticSatellitesLinked class="fr-mt-4w" :canteen-informations="canteenInformations" />
    <DiagnosticPurchasesLinked class="fr-mt-4w" />
  </div>
</template>
