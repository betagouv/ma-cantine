import { defineStore } from "pinia"
import { computed, reactive } from "vue"

const useFiltersStore = defineStore("filters", () => {
  /* Selected */
  const selected = reactive({
    year: new Date().getFullYear(),
    sectors: [],
  })
  function add(name, value) {
    selected[name] = value
  }
  function remove(name, value) {
    if (value === "") selected[name] = ""
    else selected[name] = selected[name].filter((element) => element.value !== value)
  }

  /* Exported values */
  const year = computed(() => selected.year)
  const sectors = computed(() => selected.sectors)

  /* Actions */
  function getAllSelected() {
    const list = []
    if (selected.year !== "") list.push({ name: "year", value: "", label: selected.year })
    if (selected.sectors.length > 0) {
      selected.sectors.forEach((sector) => {
        list.push({ name: "sectors", value: sector.value, label: sector.name })
      })
    }
    return list
  }

  return { add, remove, getAllSelected, year, sectors }
})

export { useFiltersStore }
