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
  const count = store.canteenPreviews.length
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
const clicSearch = () => {
  const searchValue = search.value.trim()
  isSearching.value = true
  if (searchValue === "") clearSearch()
  else searchCanteens(searchValue)
  // TODO si pas de résultat
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
    <div class="fr-col-12 fr-col-md-8">
      <h1>Bienvenue dans votre espace, {{ store.loggedUser.firstName }}</h1>
      <p class="fr-text--lead">{{ canteenSentence }}</p>
    </div>
    <div class="fr-col-12 fr-col-md-4 fr-grid-row fr-grid-row--right fr-grid-row--top">
      <AppDropdownMenu label="Gérer mes cantines" :links="links" size="medium" />
    </div>
  </section>
  <section class="ma-cantine--stick-to-footer">
    <GestionnaireCanteensCreate v-if="store.canteenPreviews.length === 0" />
    <template v-else>
      <DsfrSearchBar
        v-model="search"
        :large="true"
        label="Rechercher"
        button-text="Rechercher"
        placeholder="Rechercher une cantine par son nom, son siret, ou son siren"
        @search="clicSearch"
      />
      <AppLoader v-if="isSearching" class="fr-my-4w" />
      <GestionnaireCanteensTable v-if="!isSearching && canteensTable.length > 0" :canteens="canteensTable" />
    </template>
    <GestionnaireGuides />
  </section>
</template>
