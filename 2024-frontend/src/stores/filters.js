import { defineStore } from "pinia"
import { reactive } from "vue"

const useFiltersStore = defineStore("filters", () => {
  /* Filters paramters to send to api */
  const params = reactive({
    year: new Date().getFullYear(),
    sectors: [],
    economicModel: [],
    managementType: [],
    productionType: [],
  })

  /* Actions to update filters parameters */
  function add(name, value) {
    params[name] = value
  }
  function remove(name, value) {
    if (value === "") params[name] = ""
    else params[name] = params[name].filter((element) => element.value !== value)
  }

  /* Actions */
  function getAllSelected() {
    const list = []
    if (params.year !== "") list.push({ name: "year", value: "", label: params.year })
    if (params.economicModel.length > 0) {
      params.economicModel.forEach((economicModel) => {
        list.push({ name: "economicModel", value: economicModel.value, label: economicModel.name })
      })
    }
    if (params.managementType.length > 0) {
      params.managementType.forEach((managementType) => {
        list.push({ name: "managementType", value: managementType.value, label: managementType.name })
      })
    }
    if (params.productionType.length > 0) {
      params.productionType.forEach((productionType) => {
        list.push({ name: "productionType", value: productionType.value, label: productionType.name })
      })
    }
    if (params.sectors.length > 0) {
      params.sectors.forEach((sector) => {
        list.push({ name: "sectors", value: sector.value, label: sector.name })
      })
    }
    return list
  }

  return { add, remove, getAllSelected, params }
})

export { useFiltersStore }
