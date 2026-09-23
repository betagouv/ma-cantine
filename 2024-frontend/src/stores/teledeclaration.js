import { defineStore } from "pinia"
import { computed, ref } from "vue"
import diagnosticService from "@/services/diagnostics.js"
import canteenService from "@/services/canteens.js"
import diagnosticsFields from "@/services/diagnosticsFields.js"

const useStoreTeledeclaration = defineStore("teledeclaration", () => {
  const diagnostic = ref(null)
  const canteenSavedId = ref(null)
  const year = 2026 // Force for testing, improve ??
  const diagnosticErrors = ref([])
  const hasDiagnostic = computed(() => diagnostic.value !== null)
  const diagnosticSaved = ref(false)

  /* Init store with diagnostic of the current campaign */
  async function initStore(canteenId) {
    if (canteenSavedId.value === canteenId) return
    const diagnosticsResponse = await diagnosticService.fetchDiagnostics(canteenId)
    const diagnosticYear = diagnosticsResponse["results"].find((result) => result.year === year) || null
    if (!diagnosticYear) return
    setDiagnostic(diagnosticYear)
    setCanteenId(canteenId)
    const diagnosticCheck = await diagnosticService.checkDiagnostic(canteenId, diagnosticYear.id)
    const canteenCheck = await canteenService.checkCanteen(canteenId)
    addErrorsFromCheck({...diagnosticCheck.errors, ...canteenCheck.errors})
    diagnosticSaved.value = true
  }

  /* Save diagnostic */
  async function saveDiagnostic() {
    if (!diagnostic.value) return
    const canteenId = diagnostic.value.canteenId
    const diagnosticValues = diagnostic.value
    const response = await diagnosticService.updateDiagnostic(canteenId, diagnosticValues.id, diagnosticValues)
    if (response.status === "error") addErrorsFromServor(response.list)
    diagnosticSaved.value = true
    return response
  }

  /* Set canteen id */
  function setCanteenId(canteenId) {
    canteenSavedId.value = canteenId
  }

  /* Set all diagnostic */
  function setDiagnostic(newDiagnostic) {
    diagnostic.value = newDiagnostic
    diagnosticSaved.value = false
  }

  /* Set value for diagnostic */
  function setValue(field, value) {
    diagnostic.value[field] = value
    diagnosticSaved.value = false
  }

  /* Empty store */
  function deleteStore() {
    diagnostic.value = null
    canteenSavedId.value = null
  }

  /* Set diagnostic errors */
  function addErrorsFromCheck(errors) {
    const errorsKeys = Object.keys(errors)
    const errorsValues = Object.values(errors)
    const errorList = []
    for (let i = 0; i < errorsKeys.length; i++) {
      errorList.push({ field: errorsKeys[i], message: errorsValues[i] })
    }
    // TO FIX : Errors duplicated with "/check" errors
    diagnosticErrors.value = [...diagnosticErrors.value, ...errorList]
  }

  /* Add errors to list */
  function addErrorsFromServor(errors) {
    diagnosticErrors.value = [...diagnosticErrors.value, ...errors]
  }

  /* Clear diagnostic errors for the current campaign */
  const clearErrors = () => {
    diagnosticErrors.value = []
  }

  /* Keep only the errors related to the fields displayed on the given page */
  function getErrorsPage(pageName, canteenIsGroupe) {
    const diagnosticIsSimple = diagnostic.value.diagnosticType === "SIMPLE"
    const fieldsList = diagnosticsFields.getFieldsListFromPage(pageName, canteenIsGroupe, diagnosticIsSimple)
    return diagnosticErrors.value.filter((error) => fieldsList.includes(error.field))
  }

  /* Keep only the errors related to the fields displayed on the given page */
  function getErrorsGroup(fieldsGroupName) {
    const fieldsList = diagnosticsFields.getFieldsListFromGroup(fieldsGroupName)
    return diagnosticErrors.value.filter((error) => fieldsList.includes(error.field))
  }

  /* Has errors on field */
  function isFieldError(field) {
    return diagnosticErrors.value.some((error) => error.field === field)
  }

  /* Get error message for field */
  function getErrorMessage(field) {
    return diagnosticErrors.value.find((error) => error.field === field)?.message.join(". ")
  }

  /* Get year of the current campaign */
  function getYear() {
    return year
  }

  /* Is saved */
  function isSaved() {
    return diagnosticSaved.value
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
    addErrorsFromCheck,
    clearErrors,
    getErrorsPage,
    getErrorsGroup,
    isFieldError,
    getErrorMessage,
    isSaved,
  }
})

export { useStoreTeledeclaration }
