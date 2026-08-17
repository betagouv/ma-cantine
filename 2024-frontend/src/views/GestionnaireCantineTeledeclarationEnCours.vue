<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreCanteen } from "@/stores/canteen.js"
import documentation from "@/data/documentation.json"
import CanteenSidebarTitle from "@/components/CanteenSidebarTitle.vue"
import AppHelpCard from "@/components/AppHelpCard.vue"
import AppBlueCard from "@/components/AppBlueCard.vue"

const canteenStore = useStoreCanteen()
const currentYear = new Date().getFullYear()
const { canteenInformations } = storeToRefs(canteenStore)

/* Content */
const pageTitle = computed(() => canteenInformations.value.isGroupe ? `Télédéclaration ${currentYear}` : `Ma télédéclaration ${currentYear}`)
const firstBlocTitle = computed(() => canteenInformations.value.isGroupe ? 'Bien préparer sa télédéclaration groupée' : 'Bien préparer sa télédéclaration')
const hasPuchase = true
const purchaseAmount = "XXXX €"
const hasSatellite = computed(() => canteenInformations.value.isGroupe)
const satellitesCount = computed(() => canteenInformations.value.satellitesCount)
const emptySatellitesCount = computed(() => hasSatellite.value && satellitesCount.value == 0)

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

    <AppBlueCard
      v-if="hasSatellite"
      class="fr-mt-4w"
      title="Souhaitez-vous mettre à jour la liste de restaurants de votre groupe ?"
      alert="Optionnel : cette étape n’est pas obligatoire pour déclarer vos approvisionnements."
      :button="{
        label: 'Mettre à jour mes cantines',
        to: 'GestionnaireCantineGroupe',
      }"
    >
      <p>
        Vous avez <strong>{{ satellitesCount }} {{ satellitesCount > 1 ? 'restaurants liés' : 'restaurant lié' }}</strong> à vos approvisionnements groupés
      </p>
    </AppBlueCard>

    <AppBlueCard
      v-if="hasPuchase"
      class="fr-mt-4w"
      title="Souhaitez-vous pré-remplir votre déclaration à partir de votre suivi d’achats ?"
      alert="Optionnel : cette étape n’est pas obligatoire pour déclarer vos approvisionnements."
      :button="{
        label: 'Mettre à jour mes achats',
        to: 'PurchasesHome',
      }"
    >
      <p>
        Vous avez <strong>{{ purchaseAmount }}</strong> d’achats détectés dans votre suivi des achats. <br />
        Si vous utilisez l’Outil de Suivi des Achats (Mes achats), pour pré-remplir votre télédéclaration, assurez-vous d’avoir complété l’ensemble de vos achats de l’année précédente.
      </p>
    </AppBlueCard>

  </div>
</template>
