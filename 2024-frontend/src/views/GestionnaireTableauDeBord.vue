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
import GestionnaireCanteensTable from "@/components/GestionnaireCanteensTable.vue"
import AppDropdownMenu from "@/components/AppDropdownMenu.vue"
import AppLoader from "@/components/AppLoader.vue"
import AppJeDonneMonAvis from "@/components/AppJeDonneMonAvis.vue"

/* INTRO */
const store = useRootStore()
const canteenSentence = computed(() => {
  const count = canteensTable.value.length
  if (count === 0) return "vous n'avez pas encore de cantine"
  else if (count === 1) return "1 cantine"
  return `${count} cantines`
})

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
  }
]

/* SEARCH */
const search = ref()
const isSearching = ref(false)
const searchIsEmpty = ref(false)

const clicSearch = () => {
  isSearching.value = true
  searchCanteens()
  isSearching.value = false
}

const updateSearch = () => {
  const searchValue = search.value.trim()
  searchIsEmpty.value = searchValue === ""
  if (searchIsEmpty.value) filteredCanteens.value = []
}

const searchCanteens = () => {
  if (!search.value) return
  filteredCanteens.value = canteensTableService.searchCanteensBySiretOrSirenOrName(search.value, allCanteens.value)
  if (filteredCanteens.value.length === 0) searchIsEmpty.value = true
}

/* CANTEENS */
const lastYear = new Date().getFullYear() - 1
const filteredCanteens = ref([])
const canteensGroup = computed(() => {
  const count = allCanteens.value.filter((canteen) => canteen.productionType === "groupe").length
  const title = count > 1 ? `Vos ${count} cuisines centrales ont été transformées en groupes` : "Votre cuisine centrale a été transformée en groupe"
  return {
    displayBanner: count > 0,
    count,
    title,
  }
})

const allCanteens = computedAsync(async () => {
  const canteens = await canteenService.fetchCanteensActions(lastYear)
  const canteensFiltered = hideSatellites(canteens)
  return canteensFiltered
}, [])

const canteensTable = computed(() => {
  return filteredCanteens.value.length > 0 ? filteredCanteens.value : allCanteens.value
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
      <AppDropdownMenu label="Gérer mes cantines" :links="links" size="medium" />
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
      <div class="fr-col-12 fr-col-md-6">
        <DsfrSearchBar
          v-model="search"
          label="Rechercher"
          button-text="Rechercher"
          placeholder="Rechercher par le nom, siret ou siren de l'établissement"
          @update:modelValue="updateSearch"
          @search="clicSearch"
        />
      </div>
    </div>
    <template v-if="campaign">
      <AppLoader v-if="isSearching" class="fr-mt-2w fr-mb-4w" />
      <p class="fr-mt-2w fr-mb-4w" v-if="searchIsEmpty && search">
        Aucun résultat trouvé pour la recherche « {{ search }} »
      </p>
      <GestionnaireCanteensTable v-else :canteens="canteensTable" :campaign="campaign" />
    </template>
  </section>
  <section class="ma-cantine--bg-blue fr-py-4w">
    <GestionnaireGuides />
  </section>
  <AppJeDonneMonAvis
    url="https://jedonnemonavis.numerique.gouv.fr/Demarches/3661?button=4069"
    title="Qu'avez-vous pensé de la page Tableau de bord ?"
  />
</template>
