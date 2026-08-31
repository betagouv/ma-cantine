<script setup>
import { computed, onUnmounted, watch } from "vue"
import { storeToRefs } from "pinia"
import { useRouter } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen.js"
import { useStoreDiagnostic } from "@/stores/diagnostic.js"
import { useRootStore } from "@/stores/root.js"
import diagnosticService from "@/services/diagnostics.js"
import documentation from "@/data/documentation.json"
import CanteenSidebarTitle from "@/components/CanteenSidebarTitle.vue"
import AppHelpCard from "@/components/AppHelpCard.vue"
import DiagnosticSatellitesLinked from "@/components/DiagnosticSatellitesLinked.vue"
import DiagnosticPurchasesLinked from "@/components/DiagnosticPurchasesLinked.vue"

const rootStore = useRootStore()
const canteenStore = useStoreCanteen()
const router = useRouter()
const currentYear = new Date().getFullYear()
const lastYear = currentYear - 1
const { canteenInformations } = storeToRefs(canteenStore)

/* Diagnostic */
const diagnosticStore = useStoreDiagnostic()
const hasDiagnosticCurrentCampaign = computed(() => diagnosticStore.hasDiagnosticCurrentCampaign())
onUnmounted(() => diagnosticStore.deleteStore())
watch(
  () => canteenInformations.value.id,
  (canteenId) => { if (canteenId) diagnosticStore.initStore(canteenInformations.value.id) },
  { immediate: true }
)

/* Content */
const pageTitle = computed(() => canteenInformations.value.isGroupe ? `Télédéclaration ${currentYear}` : `Ma télédéclaration ${currentYear}`)
const firstBlocTitle = computed(() => canteenInformations.value.isGroupe ? 'Bien préparer sa télédéclaration groupée' : 'Bien préparer sa télédéclaration')
const buttonTop = computed(() => {
  const hasDiag = hasDiagnosticCurrentCampaign.value
  const label = hasDiag ? 'Reprendre ma télédéclaration' : 'Faire ma télédéclaration'
  const type = hasDiag ? 'secondary' : 'primary'
  const icon = hasDiag ? '' : 'ri-send-plane-line'
  return { label, type, icon }
})

/* Navigation */
const openTunnel = () => {
  if (!hasDiagnosticCurrentCampaign.value) createDiagnostic()
  else goToTunnel()
}

const createDiagnostic = () => {
  diagnosticService.createDiagnostic(canteenInformations.value.id, { year: lastYear })
    .then((response) => {
      if(response.status === "error") showError(response.message)
      else {
        diagnosticStore.updateDiagnosticCurrentCampaign(response)
        goToTunnel()
      }
    })
    .catch((error) => showError(error.message))
}
const goToTunnel = () => router.push({ name: "GestionnaireTunnelApproInformations" })
const showError = (message) => rootStore.notifyServerError(message)
</script>

<template>
  <CanteenSidebarTitle :title="pageTitle">
    <DsfrButton
      v-if="buttonTop"
      @click="openTunnel"
      :label="buttonTop.label"
      :[buttonTop.type]="true"
      :icon="buttonTop.icon"
    />
  </CanteenSidebarTitle>

  <div class="fr-mb-5w fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-12 fr-col-md-7">
      <h3 class="fr-h5 fr-mb-4w">{{ firstBlocTitle }}</h3>
      <p v-if="canteenInformations.isGroupe">
        Vous allez télédéclarer de manière mutualisée au sein d’une même entité de gestion. Les montants d’achats seront répartis automatiquement au prorata du nombre de couverts annuels de chaque cantine du groupe.
        <strong>Les gestionnaires des cantines n’auront pas accès aux montants d’achats, mais uniquement aux résultats (en %).</strong>
      </p>
      <p v-else>
        Réalisez votre bilan de l’année précédente sur les différents volets de la loi EGalim. La télédéclaration comporte 2 groupes de volets : les approvisionnements (simplifiés ou détaillés) et les volets thématiques.
      </p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="Appros en saisie détaillée ou simplifiée ?" content="Je rassemble les informations qui vont m’être demandées">
        <a :href="documentation.teledeclarationChecklist" target="_blank" class="fr-text-title--blue-france">Je télécharge la tcheck-list</a>
      </AppHelpCard>
    </div>
  </div>

  <div>
    <h3 class="fr-h5 fr-mb-4w">Avant de débuter :</h3>
    <ol v-if="!canteenInformations.isGroupe" class="ma-cantine--ordered-list ma-cantine--unstyled-list">
      <li class="fr-mb-2w">
        <p class="fr-mb-0">
          Consolidez vos données d’achats : consultez la <a :href="documentation.teledeclarationMatrice" target="_blank">matrice de télédéclaration</a> et l’<a :href="documentation.teledeclarationAntiseche" target="_blank">antisèche</a>
        </p>
      </li>
      <li class="fr-mb-2w">
        <p class="fr-mb-0">
          Si vous êtes en gestion concédée, coordonnez-vous avec votre prestataire pour l’obtention des données et/ou délégation de la télédéclaration : <a :href="documentation.gestionConcedee" target="_blank">voir Gestion concédée | Documentation</a>
        </p>
      </li>
      <li>
        <p class="fr-mb-0">
          Anticipez le mode de déclaration des approvisionnements simplifiés ou détaillés : <a :href="documentation.teledeclarationType" target="_blank">consulter la documentation</a>
        </p>
      </li>
    </ol>

    <DiagnosticSatellitesLinked class="fr-mt-4w" :canteen-informations="canteenInformations" />
    <DiagnosticPurchasesLinked class="fr-mt-4w" :canteen-id="canteenInformations.id" />
  </div>
</template>
