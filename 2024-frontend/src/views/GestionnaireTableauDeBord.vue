<script setup>
import { ref, computed } from "vue"
import { computedAsync } from "@vueuse/core"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"

import GestionnaireGuides from "@/components/GestionnaireGuides.vue"
import GestionnaireCanteensCreate from "@/components/GestionnaireCanteensCreate.vue"
import GestionnaireCanteensTable from "@/components/GestionnaireCanteensTable.vue"
import AppDropdownMenu from "@/components/AppDropdownMenu.vue"
import AppLoader from "@/components/AppLoader.vue"

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
  const searchValue = search.value.trim()
  isSearching.value = true
  searchIsEmpty.value = false
  if (searchValue === "") clearSearch()
  else {
    searchCanteens(searchValue)
    if (filteredCanteens.value.length === 0) searchIsEmpty.value = true
  }
  isSearching.value = false
}

const clearSearch = () => {
  filteredCanteens.value = []
}

const searchCanteens = (searchValue) => {
  filteredCanteens.value = allCanteens.value.filter((canteen) => {
    if (canteen.siret && canteen.siret.indexOf(searchValue) === 0) return true
    if (canteen.sirenUniteLegale && canteen.sirenUniteLegale.indexOf(searchValue) === 0) return true
    if (canteen.name.indexOf(searchValue) > 0) return true
  })
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
          @search="clicSearch"
        />
      </div>
    </div>
    <AppLoader v-if="isSearching" class="fr-mt-2w fr-mb-4w" />
    <p class="fr-mt-2w fr-mb-4w" v-if="searchIsEmpty">Aucun résultat trouvé pour la recherche « {{ search }} »</p>
    <GestionnaireCanteensTable v-else :canteens="canteensTable" />
  </section>
  <GestionnaireGuides class="ma-cantine--stick-to-footer" />
</template>
