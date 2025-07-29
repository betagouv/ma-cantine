import { defineStore } from "pinia"
import { ref, reactive } from "vue"

const useStoreFilters = defineStore("filters", () => {
  /* Default filter */
  const currentYear = new Date().getFullYear()

  /* Filters parameters to send to api */
  const params = reactive({
    year: currentYear,
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

  /* User filter selection ordered preserved */
  const selection = ref([{ name: "year", value: currentYear, label: currentYear }])

  /* Actions to update filters parameters */
  function set(name, value) {
    updateSelection(name, value)
    params[name] = value
  }

  function remove(name, value) {
    params[name] = name === "year" ? "" : params[name].filter((element) => element.value !== value)
    removeFromSelection(name, value)
  }

  /* Action to get a filter parameters values */
  function get(name) {
    return name === "year" ? params.year : [...params[name]]
  }

  /* Action to get all filters */
  function getAll() {
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
    selection.value.splice(indexToRemove, 1)
  }

  function updateSelection(name, value) {
    const isRemovingFilled = name !== "year" && params[name].length > value.length
    if (isRemovingFilled) removeFromSelection(name, findValueToRemove(name, value))
    else addToSelection(name, value)
  }

  function getSelection() {
    return selection.value
  }

  return { set, remove, getSelection, get, getAll }
})

export { useStoreFilters }
