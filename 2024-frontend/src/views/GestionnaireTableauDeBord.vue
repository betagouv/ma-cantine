<script setup>
import { ref, computed } from "vue"
import { useRootStore } from "@/stores/root"
import GestionnaireGuides from "@/components/GestionnaireGuides.vue"
import GestionnaireCanteensCreate from "@/components/GestionnaireCanteensCreate.vue"
import GestionnaireCanteensTable from "@/components/GestionnaireCanteensTable.vue"
import AppDropdownMenu from "@/components/AppDropdownMenu.vue"
import AppLoader from "@/components/AppLoader.vue"

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
const searchCanteen = () => {
  isSearching.value = true
  console.log("searchCanteen", search.value)
}
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
        @search="searchCanteen"
      />
      <AppLoader v-if="isSearching" class="fr-my-4w" />
      <GestionnaireCanteensTable v-if="!isSearching" />
    </template>
    <GestionnaireGuides />
  </section>
</template>
