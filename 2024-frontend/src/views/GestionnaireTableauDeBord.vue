<script setup>
import { ref, computed } from "vue"
import { computedAsync } from "@vueuse/core"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"
import stringService from "@/services/strings.js"

import GestionnaireGuides from "@/components/GestionnaireGuides.vue"
import GestionnaireCanteensCreate from "@/components/GestionnaireCanteensCreate.vue"
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
    to: { name: "GestionnaireCantineAjouter" },
    label: "Créer une cantine",
  },
  {
    to: { name: "GestionnaireImportCantines" },
    label: "Importer des cantines",
  },
  {
    to: { name: "GestionnaireImportAchats" },
    label: "Importer des achats",
  },
  {
    to: { name: "GestionnaireImport" },
    label: "Importer un bilan simple",
  },
  {
    to: { name: "GestionnaireImport" },
    label: "Importer un bilan détaillé",
  },
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
  const searchValue = search.value.trim()
  filteredCanteens.value = allCanteens.value.filter((canteen) => {
    if (canteen.siret && canteen.siret.indexOf(searchValue) === 0) return true
    if (canteen.sirenUniteLegale && canteen.sirenUniteLegale.indexOf(searchValue) === 0) return true
    if (stringService.checkIfContains(canteen.name, searchValue)) return true
  })
  if (filteredCanteens.value.length === 0) searchIsEmpty.value = true
}

/* CANTEENS */
const lastYear = new Date().getFullYear() - 1
const filteredCanteens = ref([])
const allCanteens = computedAsync(async () => {
  return await canteenService.fetchCanteensActions(lastYear)
}, [])
const canteensTable = computed(() => {
  return filteredCanteens.value.length > 0 ? filteredCanteens.value : allCanteens.value
})
</script>

<template>
  <section class="fr-grid-row">
    <h1 class="fr-col-12 fr-col-md-6">Bienvenue dans votre espace, {{ store.loggedUser.firstName }}</h1>
    <div class="fr-col-12 fr-col-md-6 fr-grid-row fr-grid-row--right fr-grid-row--top">
      <AppDropdownMenu label="Gérer mes cantines" :links="links" size="medium" />
    </div>
  </section>
  <GestionnaireCanteensCreate v-if="store.canteenPreviews.length === 0" />
  <section v-else>
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
    <AppLoader v-if="isSearching" class="fr-mt-2w fr-mb-4w" />
    <p class="fr-mt-2w fr-mb-4w" v-if="searchIsEmpty && search">
      Aucun résultat trouvé pour la recherche « {{ search }} »
    </p>
    <GestionnaireCanteensTable v-else :canteens="canteensTable" />
  </section>
  <section class="ma-cantine--bg-blue fr-py-4w">
    <GestionnaireGuides />
  </section>
  <AppJeDonneMonAvis
    url="https://jedonnemonavis.numerique.gouv.fr/Demarches/3661?button=4069"
    title="Qu'avez-vous pensé de la page Tableau de bord ?"
  />
</template>
