import { defineStore } from "pinia"
import { computed, reactive } from "vue"

const useFiltersStore = defineStore("filters", () => {
  /* Selected */
  const selected = reactive({
    year: new Date().getFullYear(),
  })
  function update(name, value) {
    selected[name] = value
  }

  /* Exported values */
  const year = computed(() => selected.year)

  /* Actions */
  function getAllSelected() {
    const list = []
    if (selected.year !== "") list.push({ name: "year", value: selected.year })
    return list
  }

  return { update, getAllSelected, year }
})

export { useFiltersStore }
