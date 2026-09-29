<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useRouter } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen.js"
import { useStoreTeledeclaration } from "@/stores/teledeclaration.js"
import { useRootStore } from "@/stores/root.js"
import diagnosticService from "@/services/diagnostics.js"
import documentation from "@/data/documentation.json"
import CanteenSidebarTitle from "@/components/CanteenSidebarTitle.vue"
import AppHelpCard from "@/components/AppHelpCard.vue"
import DiagnosticSatellitesLinked from "@/components/DiagnosticSatellitesLinked.vue"
import DiagnosticPurchasesLinked from "@/components/DiagnosticPurchasesLinked.vue"
import DiagnosticSummaryAccordions from "@/components/DiagnosticSummaryAccordions.vue"

const rootStore = useRootStore()
const canteenStore = useStoreCanteen()
const router = useRouter()
const currentYear = new Date().getFullYear()
const { canteenInformations } = storeToRefs(canteenStore)

/* Teledeclaration */
const teledeclarationStore = useStoreTeledeclaration()
const { hasDiagnostic, canteenAction } = storeToRefs(teledeclarationStore)
const year = teledeclarationStore.getYear()

/* Content */
const pageTitle = computed(() => canteenInformations.value.isGroupe ? `Télédéclaration ${currentYear}` : `Ma télédéclaration ${currentYear}`)
const buttonTop = computed(() => {
  switch (true) {
    case canteenAction.value === "40_teledeclare":
      return { label: 'Télédéclarer', icon: 'ri-send-plane-line', pageName: "GestionnaireTunnelApproRecapitulatif" }
    case hasDiagnostic.value:
      return { label: 'Reprendre ma télédéclaration', icon: 'fr-icon-edit-fill', pageName: "GestionnaireTunnelApproInformations" }
    default:
      return { label: 'Faire ma télédéclaration', icon: 'ri-send-plane-line' }
  }
})

/* Navigation */
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
  <CanteenSidebarTitle :title="pageTitle">
    <DsfrButton
      v-if="buttonTop"
      primary
      @click="openTunnel(buttonTop.pageName)"
      :label="buttonTop.label"
      :icon="buttonTop.icon"
    />
  </CanteenSidebarTitle>

  <div class="fr-mb-5w fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-12 fr-col-md-7">
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
      <AppHelpCard title="Infos utiles pour consolider vos données">
        <p class="fr-mb-1w">
          <a :href="documentation.teledeclarationMatrice" target="_blank" class="fr-text-title--blue-france">La matrice de télédéclaration</a>
        </p>
        <p class="fr-mb-1w">
          <a :href="documentation.teledeclarationChecklist" target="_blank" class="fr-text-title--blue-france">L’antisèche</a>
        </p>
        <p class="fr-mb-1w">
          <a :href="documentation.gestionConcedee" target="_blank" class="fr-text-title--blue-france">Gestion concédée : bien m’organiser</a>
        </p>
      </AppHelpCard>
    </div>
  </div>
  <DiagnosticSummaryAccordions v-if="hasDiagnostic" />
  <div>
    <h3 class="fr-h5 fr-mb-4w">Avant de débuter :</h3>
    <DiagnosticSatellitesLinked class="fr-mt-4w" :canteen-informations="canteenInformations" />
    <DiagnosticPurchasesLinked class="fr-mt-4w" />
  </div>
</template>
