<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const tiles = ref([
  {
    title: "Importer des cantines",
    name: "GestionnaireImportCantines",
    description: "Vous voulez créer ou mettre à jour des cantines.",
    tags: ["Excel", "CSV"],
  },
  {
    title: "Importer des achats",
    name: "GestionnaireImportAchats",
    description: "Vous voulez importer des données d'achat pour des cantines existantes.",
    tags: ["CSV"],
  },
])
</script>

<template>
  <div>
    <h1>{{ route.meta.title }}</h1>
    <ul class="ma-cantine--unstyled-list fr-grid-row fr-grid-row--gutters">
      <li v-for="tile in tiles" :key="tile.name" class="fr-col-12 fr-col-md-4">
        <DsfrTile :title="tile.title" :to="{ name: tile.name }" :description="tile.description">
          <template #header>
            <DsfrBadge v-for="tag in tile.tags" :key="tag" :label="tag" class="fr-mr-1v" :no-icon="true" />
          </template>
        </DsfrTile>
      </li>
    </ul>
  </div>
</template>
