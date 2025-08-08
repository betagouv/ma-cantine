<script setup>
import { ref, computed, onMounted } from "vue"
import { useRoute } from "vue-router"
import { useStoreFilters } from "@/stores/filters"
import { getYearsOptions } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const options = ref(getYearsOptions())
const storeFilters = useStoreFilters()
const yearSelected = computed(() => storeFilters.getParam("year"))
const route = useRoute()

/* Select from url */
onMounted(() => {
  const query = route.query
  if (query.year) storeFilters.set("year", Number(query.year))
})
</script>

<template>
  <FilterByBase label="Années">
    <DsfrRadioButtonSet
      :modelValue="yearSelected"
      @update:modelValue="storeFilters.set('year', $event)"
      :options="options"
      small
    />
  </FilterByBase>
</template>
