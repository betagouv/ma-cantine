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
    departements: [],
    epcis: [],
    pats: [],
  })

  /* Actions to update filters parameters */
  function add(name, value) {
    params[name] = value
  }
  function remove(name, value) {
    if (value === "") params[name] = ""
    else params[name] = params[name].filter((element) => element.value !== value)
  }

  /* Action to get all parameters with non empty */
  function getFilled() {
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
    if (params.regions.length > 0) {
      params.regions.forEach((region) => {
        list.push({ name: "regions", value: region.value, label: region.name })
      })
    }
    if (params.departements.length > 0) {
      params.departements.forEach((departement) => {
        list.push({ name: "departements", value: departement.value, label: departement.name })
      })
    }
    if (params.epcis.length > 0) {
      params.epcis.forEach((epci) => {
        list.push({ name: "epcis", value: epci.value, label: epci.name })
      })
    }
    if (params.pats.length > 0) {
      params.pats.forEach((pat) => {
        list.push({ name: "pats", value: pat.value, label: pat.name })
      })
    }
    return list
  }

  return { add, remove, getFilled, params }
})

export { useStoreFilters }
