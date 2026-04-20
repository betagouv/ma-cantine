<script setup>
import { ref, computed } from "vue"
import { computedAsync } from "@vueuse/core"
import { useRootStore } from "@/stores/root"
import documentation from "@/data/documentation.json"
import canteenService from "@/services/canteens.js"
import campaignService from "@/services/campaigns.js"
import canteensTableService from "@/services/canteensTable.js"
import GestionnaireGuides from "@/components/GestionnaireGuides.vue"
import GestionnaireEmptyCanteen from "@/components/GestionnaireEmptyCanteen.vue"
import CanteensTable from "@/components/CanteensTable.vue"
import CanteenModalExport from "@/components/CanteenModalExport.vue"
import AppDropdownMenu from "@/components/AppDropdownMenu.vue"
import AppLoader from "@/components/AppLoader.vue"
import AppJeDonneMonAvis from "@/components/AppJeDonneMonAvis.vue"
import FilterByBase from "@/components/FilterByBase.vue"

/* DATA */
const store = useRootStore()
const lastYear = new Date().getFullYear() - 1

/* BUTTON */
const links = [
  {
    to: { name: "GestionnaireCantineRestaurantAjouter" },
    label: "Ajouter une cantine",
  },
  {
    to: { name: "GestionnaireCantineGroupeAjouter" },
    label: "Ajouter un groupe de restaurants satellites",
  },
  {
    to: { name: "GestionnaireImport" },
    label: "Importer des données",
  },
  {
    emitEvent: 'clickExport',
    label: "Exporter des données",
  }
]

const modalExportOpened = ref(false)
const clickDropdownMenu = (emitEvent) => {
  if (emitEvent === 'clickExport') modalExportOpened.value = true
}

/* SEARCH AND FILTERS */
const search = ref()
const filterTeledeclaration = ref('')

/* CANTEENS */
const allCanteens = computedAsync(async () => {
  const allCanteens = await canteenService.fetchCanteensActions(lastYear)
  return hideSatellites(allCanteens)  // Always hide satellites on this page
}, [])

const canteensGroup = computed(() => {
  const count = allCanteens.value.filter((canteen) => canteen.productionType === "groupe").length
  const title = count > 1 ? `Vos ${count} cuisines centrales ont été transformées en groupes` : "Votre cuisine centrale a été transformée en groupe"
  return {
    displayBanner: count > 0,
    count,
    title,
  }
})

const canteenSentence = computed(() => {
  const count = canteensTable.value.length
  if (count === 0 && !tableIsEmpty.value) return "vous n'avez pas encore de cantine"
  else if (count === 0 && tableIsEmpty.value) return "0 cantine"
  else if (count === 1) return "1 cantine"
  return `${count} cantines`
})

const canteensTable = computed(() => {
  let canteensToDisplay = [...allCanteens.value]
  if (search.value) canteensToDisplay = canteensTableService.searchCanteensBySiretOrSirenOrName(search.value, canteensToDisplay)
  if (filterTeledeclaration.value) {
    const teledeclarationFilterValue = filterTeledeclaration.value === '1'
    canteensToDisplay = canteensTableService.filterCanteensByTeledeclaration(teledeclarationFilterValue, canteensToDisplay)
  }
  return canteensToDisplay
})

const tableIsEmpty = computed(() => {
  const hasFilterOrSearchActive = search.value || filterTeledeclaration.value
  const noCanteenToDisplay = canteensTable.value.length === 0
  return hasFilterOrSearchActive && noCanteenToDisplay
})

const hideSatellites = (canteens) => {
  const canteensGroup = canteens.filter((canteen) => canteen.productionType === "groupe").map((canteen) => canteen.id)
  const canteensSatFiltered = canteens.filter((canteen) => {
    const inMyGroup = canteen.productionType === "site_cooked_elsewhere" && canteensGroup.includes(canteen.groupe)
    return inMyGroup ? false : true
  })
  return canteensSatFiltered
}

/* CAMPAIGN */
const campaign = computedAsync(async () => {
  return await campaignService.getYearCampaignDates(lastYear)
}, false)
</script>

<template>
  <section class="fr-grid-row">
    <h1 class="fr-col-12 fr-col-md-6">Bienvenue dans votre espace, {{ store.loggedUser.firstName }}</h1>
    <div class="fr-col-12 fr-col-md-6 fr-grid-row fr-grid-row--right fr-grid-row--top">
      <AppDropdownMenu label="Gérer mes cantines" :links="links" size="medium" @click="clickDropdownMenu" />
    </div>
  </section>
  <DsfrAlert v-if="canteensGroup.displayBanner > 0" :title="canteensGroup.title" class="fr-mb-4w">
    <p>Vous pouvez requalifier vos groupes directement depuis ce tableau de bord, <a :href="documentation.groupesRestaurantsSatellites" target="_blank">découvrez comment faire</a></p>
  </DsfrAlert>
  <GestionnaireEmptyCanteen v-if="store.canteenPreviews.length === 0" />
  <section v-else-if="store.canteenPreviews.length > 0 && campaign">
    <div class="fr-grid-row">
      <div class="fr-col-12 fr-col-md-6">
        <p class="fr-mb-0 fr-text--lead">{{ canteenSentence }}</p>
      </div>
      <div class="fr-col-12 fr-col-md-6 fr-grid-row fr-grid-row--middle fr-grid-row--right">
        <FilterByBase label="Filtrer par" class="fr-mr-1w">
          <p class="fr-mb-2w">Statut du bilan</p>
          <DsfrRadioButtonSet
            v-model="filterTeledeclaration"
            :options="[{ label: 'Bilan télédéclaré', value: '1'}, { label: 'Bilan non télédéclaré', value: '0'}]"
            class="fr-mb-0"
            small
            inline
          />
          <DsfrButton 
            v-show="filterTeledeclaration" @click="filterTeledeclaration = null" 
            icon="fr-icon-close-circle-line" 
            size="small"
            tertiary 
          >
            Désélectionner
          </DsfrButton>
        </FilterByBase>
        <DsfrSearchBar
          v-model="search"
          label="Rechercher"
          button-text="Rechercher"
          placeholder="Chercher un établissement par nom, siret ou siren"
          class="gestionnaire-tableau-de-bord__search"
        />
      </div>
    </div>
    <template v-if="campaign">
      <p class="fr-mt-2w fr-mb-4w" v-if="tableIsEmpty">
        Aucun résultat trouvé pour la recherche « {{ search }} »
      </p>
      <CanteensTable v-else :canteens="canteensTable" :campaign="campaign" />
    </template>
  </section>
  <section class="ma-cantine--bg-blue fr-py-4w">
    <GestionnaireGuides />
  </section>
  <AppJeDonneMonAvis
    url="https://jedonnemonavis.numerique.gouv.fr/Demarches/3661?button=4069"
    title="Qu'avez-vous pensé de la page Tableau de bord ?"
  />
  <CanteenModalExport :opened="modalExportOpened" @close="modalExportOpened = false" />
</template>

<style lang="scss">
.gestionnaire-tableau-de-bord {
  &__search {
    flex-grow: 1;
  }
}
</style>
