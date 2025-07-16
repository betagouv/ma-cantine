import { defineStore } from "pinia"
import { reactive } from "vue"

const useStoreFilters = defineStore("filters", () => {
  /* Filters parameters to send to api */
  const params = reactive({
    year: new Date().getFullYear(),
    sectors: [],
    economicModel: [],
    managementType: [],
    productionType: [],
    regions: [],
    departments: [],
    epcis: [],
    pats: [],
    cities: [],
  })

  /* Actions to update filters parameters */
  function add(name, value) {
    params[name] = value
  }
  function remove(name, value) {
    if (value === "") params[name] = ""
    else params[name] = params[name].filter((element) => element.value !== value)
  }

  /* Action to get a filter parameters values */
  function get(name) {
    return name === "year" ? params.year : [...params[name]]
  }

  /* Action to get all parameters with non empty */
  function getFilled() {
    const list = []
    if (params.year !== "") list.push({ name: "year", value: "", label: params.year })
    if (params.economicModel.length > 0) {
      params.economicModel.forEach((economicModel) => {
        list.push({ name: "economicModel", value: economicModel.value, label: economicModel.label })
      })
    }
    if (params.managementType.length > 0) {
      params.managementType.forEach((managementType) => {
        list.push({ name: "managementType", value: managementType.value, label: managementType.label })
      })
    }
    if (params.productionType.length > 0) {
      params.productionType.forEach((productionType) => {
        list.push({ name: "productionType", value: productionType.value, label: productionType.label })
      })
    }
    if (params.sectors.length > 0) {
      params.sectors.forEach((sector) => {
        list.push({ name: "sectors", value: sector.value, label: sector.label })
      })
    }
    if (params.regions.length > 0) {
      params.regions.forEach((region) => {
        list.push({ name: "regions", value: region.value, label: region.label })
      })
    }
    if (params.departments.length > 0) {
      params.departments.forEach((department) => {
        list.push({ name: "departments", value: department.value, label: department.label })
      })
    }
    if (params.epcis.length > 0) {
      params.epcis.forEach((epci) => {
        list.push({ name: "epcis", value: epci.value, label: epci.label })
      })
    }
    if (params.pats.length > 0) {
      params.pats.forEach((pat) => {
        list.push({ name: "pats", value: pat.value, label: pat.label })
      })
    }
    if (params.cities.length > 0) {
      params.cities.forEach((city) => {
        list.push({ name: "cities", value: city.value, label: city.label })
      })
    }
    return list
  }

  return { add, remove, getFilled, get }
})

export { useStoreFilters }
