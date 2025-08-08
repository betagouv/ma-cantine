<script setup>
import { ref, computed, onMounted } from "vue"
import { useRoute } from "vue-router"
import { useStoreFilters } from "@/stores/filters"
import { getSectorsOptions } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const storeFilters = useStoreFilters()
const sectorsSelected = computed(() => storeFilters.getParam("sectors"))
const route = useRoute()

/* Get sectors */
const sectors = ref([])

/* Search */
const search = ref("")
const options = computed(() => {
  if (sectors.value.length === 0) return []
  if (search.value === "") return sectors.value
  const searchedSectors = sectors.value.filter((sector) => {
    const sectorLabel = sector.label.toLowerCase()
    const stringSearched = search.value.toLowerCase()
    return sectorLabel.indexOf(stringSearched) >= 0
  })
  return searchedSectors
})

/* Save from url while waiting for sectors */
onMounted(() => {
  const query = route.query
  getSectorsOptions().then((response) => {
    sectors.value = response
    if (query.sectors) {
      const hasMultipleValues = typeof query.sectors !== "string"
      const sectorsId = hasMultipleValues ? query.sectors.map((value) => Number(value)) : [Number(query.sectors)]
      storeFilters.setFromQuery("sectors", sectorsId, response)
    }
  })
})
</script>

<template>
  <FilterByBase label="Secteurs">
    <DsfrSearchBar v-model="search" placeholder="Rechercher un secteur" />
    <DsfrCheckboxSet
      :modelValue="sectorsSelected"
      @update:modelValue="storeFilters.set('sectors', $event)"
      :options="options"
      small
    />
  </FilterByBase>
</template>
