import { defineStore } from "pinia"
import { computed, reactive } from "vue"

const useFiltersStore = defineStore("filters", () => {
  /* Selection */
  const selected = reactive({
    year: new Date().getFullYear(),
    sectors: [],
    economicModel: [],
    managementType: [],
    productionType: [],
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
  const economicModel = computed(() => selected.economicModel)
  const managementType = computed(() => selected.managementType)
  const productionType = computed(() => selected.productionType)

  /* Actions */
  function getAllSelected() {
    const list = []
    if (selected.year !== "") list.push({ name: "year", value: "", label: selected.year })
    if (selected.economicModel.length > 0) {
      selected.economicModel.forEach((economicModel) => {
        list.push({ name: "economicModel", value: economicModel.value, label: economicModel.name })
      })
    }
    if (selected.managementType.length > 0) {
      selected.managementType.forEach((managementType) => {
        list.push({ name: "managementType", value: managementType.value, label: managementType.name })
      })
    }
    if (selected.productionType.length > 0) {
      selected.productionType.forEach((productionType) => {
        list.push({ name: "productionType", value: productionType.value, label: productionType.name })
      })
    }
    if (selected.sectors.length > 0) {
      selected.sectors.forEach((sector) => {
        list.push({ name: "sectors", value: sector.value, label: sector.name })
      })
    }
    return list
  }

  return { add, remove, getAllSelected, year, sectors, economicModel, managementType, productionType }
})

export { useFiltersStore }
