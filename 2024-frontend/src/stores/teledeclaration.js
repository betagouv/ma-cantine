import { defineStore } from "pinia"
import { computed, ref } from "vue"
import diagnosticService from "@/services/diagnostics.js"

const useStoreTeledeclaration = defineStore("teledeclaration", () => {
  const diagnostic = ref(null)
  const canteenSavedId = ref(null)
  const year = 2026 // Force for testing, improve ??
  const diagnosticErrors = ref([])
  const hasDiagnostic = computed(() => diagnostic.value !== null)

  /* Init store with diagnostic of the current campaign */
  async function initStore(canteenId) {
    if (canteenSavedId.value === canteenId) return
    const response = await diagnosticService.fetchDiagnostics(canteenId)
    diagnostic.value = response["results"].find((result) => result.year === year) || null
    canteenSavedId.value = canteenId
  }

  /* Save diagnostic */
  async function saveDiagnostic() {
    if (!diagnostic.value) return
    const response = await diagnosticService.updateDiagnostic(
      diagnostic.value.canteenId,
      diagnostic.value.id,
      diagnostic.value
    )
    return response
  }

  /* Update diagnostic */
  function setDiagnostic(newDiagnostic) {
    diagnostic.value = newDiagnostic
  }

  /* Set value for diagnostic */
  function setValue(field, value) {
    diagnostic.value[field] = value
  }

  /* Empty store */
  function deleteStore() {
    diagnostic.value = null
    canteenSavedId.value = null
  }

  /* Save diagnostic errors for the current campaign */
  function saveErrors(errors) {
    diagnosticErrors.value = errors
  }

  /* Clear diagnostic errors for the current campaign */
  const clearErrors = () => {
    diagnosticErrors.value = []
  }

  /* Get year of the current campaign */
  function getYear() {
    return year
  }

  return {
    diagnostic,
    diagnosticErrors,
    hasDiagnostic,
    initStore,
    deleteStore,
    getYear,
    setDiagnostic,
    setValue,
    saveDiagnostic,
    saveErrors,
    clearErrors,
  }
})

export { useStoreTeledeclaration }
