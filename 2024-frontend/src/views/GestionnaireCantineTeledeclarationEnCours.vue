<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreCanteen } from "@/stores/canteen.js"
import documentation from "@/data/documentation.json"
import CanteenSidebarTitle from "@/components/CanteenSidebarTitle.vue"
import AppHelpCard from "@/components/AppHelpCard.vue"

const canteenStore = useStoreCanteen()
const currentYear = new Date().getFullYear()
const { canteenInformations } = storeToRefs(canteenStore)

/* Content */
const pageTitle = computed(() => canteenInformations.value.isGroupe ? `Télédéclaration ${currentYear}` : `Ma télédéclaration ${currentYear}`)
const firstBlocTitle = computed(() => canteenInformations.value.isGroupe ? 'Bien préparer sa télédéclaration groupée' : 'Bien préparer sa télédéclaration')

const gotToAppro = () => {
  console.log("gotToAppro")
}
</script>

<template>
  <CanteenSidebarTitle :title="pageTitle">
    <DsfrButton
      @click="gotToAppro"
      label="Faire ma télédéclaration"
      icon="ri-send-plane-line"
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

</template>
