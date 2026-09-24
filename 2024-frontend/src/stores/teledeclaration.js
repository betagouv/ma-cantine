import { defineStore } from "pinia"
import { computed, ref } from "vue"
import diagnosticService from "@/services/diagnostics.js"
import canteenService from "@/services/canteens.js"
import diagnosticsFields from "@/services/diagnosticsFields.js"
import teledeclarationFields from "@/data/teledeclaration.json"

const useStoreTeledeclaration = defineStore("teledeclaration", () => {
  const diagnostic = ref(null)
  const canteenSavedId = ref(null)
  const year = 2026 // Force for testing, improve ??
  const diagnosticErrors = ref([])
  const hasDiagnostic = computed(() => diagnostic.value !== null)
  const isSaved = ref(true)

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
  }

  /* Save diagnostic */
  async function saveDiagnostic() {
    if (!diagnostic.value) return
    const canteenId = diagnostic.value.canteenId
    const diagnosticValues = diagnostic.value
    const response = await diagnosticService.updateDiagnostic(canteenId, diagnosticValues.id, diagnosticValues)
    if (response.status === "error") replaceErrors(response.list)
    else isSaved.value = true
    return response
  }

  /* Save only the given fields of the diagnostic */
  async function updateMealCount() {
    if (!diagnostic.value) return
    const canteenId = diagnostic.value.canteenId
    const valeurTotalFieldName = teledeclarationFields.groups["valeurTotale"][0]
    const coutRepasFieldName = teledeclarationFields.groups["coutRepas"][0]
    const response = await diagnosticService.updateDiagnostic(canteenId, diagnostic.value.id, { [valeurTotalFieldName]: diagnostic.value[valeurTotalFieldName] })
    if (response.status === "error") replaceErrors(response.list)
    else setValue(coutRepasFieldName, response[coutRepasFieldName])
    return response
  }

  /* Set canteen id */
  function setCanteenId(canteenId) {
    canteenSavedId.value = canteenId
  }

  /* Set all diagnostic */
  function setDiagnostic(newDiagnostic) {
    diagnostic.value = newDiagnostic
    isSaved.value = true
  }

  /* Set value for diagnostic */
  function setValue(field, value) {
    diagnostic.value[field] = value
    isSaved.value = false
  }

  /* Empty store */
  function deleteStore() {
    diagnostic.value = null
    canteenSavedId.value = null
    isSaved.value = true
  }

  /* Format errors object into a list of { field, message } */
  function formatErrorToList(errors) {
    const errorsKeys = Object.keys(errors)
    const errorsValues = Object.values(errors)
    const errorList = []
    for (let i = 0; i < errorsKeys.length; i++) {
      errorList.push({ field: errorsKeys[i], message: errorsValues[i] })
    }
    return errorList
  }

  /* Format and add diagnostic errors */
  function addErrorsFromCheck(errors) {
    const errorList = formatErrorToList(errors)
    clearErrors()
    setErrors(errorList)
  }

  /* Replace errors list */
  function setErrors(newErrors) {
    diagnosticErrors.value = newErrors
  }

  /* Replace in errors list */
  function replaceErrors(newErrors) {
    const updatedErrors = diagnosticErrors.value
    for (let i = 0; i < newErrors.length; i++) {
      const newError = newErrors[i]
      clearError(newError.field)
      const oldErrorIndex = updatedErrors.findIndex((error) => error.field === newError.field)
      if (oldErrorIndex !== -1) updatedErrors.splice(oldErrorIndex, 1)
      updatedErrors.push(newError)
    }
    setErrors(updatedErrors)
  }

  /* Clear diagnostic errors for the current campaign */
  const clearErrors = () => {
    diagnosticErrors.value = []
  }

  /* Clear one error */
  const clearError = (field) => {
    diagnosticErrors.value = diagnosticErrors.value.filter((error) => error.field !== field)
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

  return {
    diagnostic,
    diagnosticErrors,
    hasDiagnostic,
    isSaved,
    initStore,
    deleteStore,
    getYear,
    setDiagnostic,
    setValue,
    saveDiagnostic,
    updateMealCount,
    addErrorsFromCheck,
    clearErrors,
    getErrorsPage,
    getErrorsGroup,
    isFieldError,
    getErrorMessage,
  }
})

export { useStoreTeledeclaration }
