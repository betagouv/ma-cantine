import { defineStore } from "pinia"
import { reactive } from "vue"

const useStoreFilters = defineStore("filters", () => {
  /* Setup */
  const currentYear = new Date().getFullYear()

  /* Filters parameters to send to api */
  const params = reactive({
    year: [{ value: currentYear, label: currentYear }],
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
  function set(name, value) {
    params[name] = value
  }
  function remove(name, value) {
    params[name] = params[name].filter((element) => element.value !== value)
  }

  /* Action to get a filter parameters values */
  function get(name) {
    return params[name]
  }

  /* Action to get all filters */
  function getAll() {
    return params
  }

  /* Action to get all parameters with non empty */
  function getFilled() {
    const filledParams = []
    Object.keys(params).forEach((key) => {
      if (params[key].length > 0) {
        params[key].forEach((option) => {
          filledParams.push({ name: key, value: option.value, label: option.label })
        })
      }
    })
    return filledParams
  }

  return { set, remove, getFilled, get, getAll }
})

export { useStoreFilters }
