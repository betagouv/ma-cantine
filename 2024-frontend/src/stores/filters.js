import { defineStore } from "pinia"
import { ref, reactive } from "vue"

const useStoreFilters = defineStore("filters", () => {
  /* Default filter */
  const lastYear = new Date().getFullYear() - 1

  /* Filters parameters */
  const params = reactive({
    year: lastYear,
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

  /* Filters selection with user order preserved */
  const selection = ref([{ name: "year", value: lastYear, label: lastYear }])

  /* Actions to update filters params */
  function set(name, value) {
    updateSelection(name, value)
    params[name] = value
  }

  function remove(name, value) {
    params[name] = name === "year" ? "" : params[name].filter((element) => element.value !== value)
    removeFromSelection(name, value)
  }

  /* Action to get filter params values */
  function getParam(name) {
    return name === "year" ? params.year : [...params[name]]
  }

  function getAllParams() {
    return params
  }

  /* Actions to update user selection */
  function findValueToRemove(name, newValue) {
    const paramsToRemove = params[name].filter((oldValue) => !newValue.includes(oldValue))
    return paramsToRemove[0].value
  }

  function addToSelection(name, value) {
    const isYear = name === "year"
    const lastValueAdded = !isYear ? value[value.length - 1] : []
    if (isYear) removeFromSelection(name, value)
    const valueToAdd = {
      name: name,
      value: isYear ? value : lastValueAdded.value,
      label: isYear ? value : lastValueAdded.label,
    }
    selection.value.push(valueToAdd)
  }

  function removeFromSelection(name, value) {
    const indexToRemove =
      name === "year"
        ? selection.value.findIndex((element) => element.name === "year")
        : selection.value.findIndex((element) => element.name === name && element.value === value)
    if (indexToRemove >= 0) selection.value.splice(indexToRemove, 1)
  }

  function updateSelection(name, value) {
    const isRemovingFilled = name !== "year" && params[name].length > value.length
    if (isRemovingFilled) removeFromSelection(name, findValueToRemove(name, value))
    else addToSelection(name, value)
  }

  function getSelection() {
    return selection.value
  }

  function getSelectionLabels() {
    return selection.value.map((item) => item.label).join(", ")
  }

  /* Action to get params readable for url query */
  function getQueryParams() {
    const keys = Object.keys(params)
    let query = {}
    for (let i = 0; i < keys.length; i++) {
      const name = keys[i]
      const isYear = name === "year"
      const value = params[name]
      query[name] = isYear ? value : value.map((element) => element.value)
    }
    return query
  }

  return { set, remove, getSelection, getSelectionLabels, getParam, getAllParams, getQueryParams }
})

export { useStoreFilters }
