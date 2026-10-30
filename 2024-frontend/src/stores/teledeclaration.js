import { defineStore } from "pinia"
import { computed, ref } from "vue"
import { useRootStore } from "@/stores/root.js"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary.js"
import diagnosticService from "@/services/diagnostics.js"
import canteenService from "@/services/canteens.js"
import teledeclarationFields from "@/services/teledeclarationFields.js"

const useStoreTeledeclaration = defineStore("teledeclaration", () => {
  const diagnostic = ref(null)
  const canteenSavedId = ref(null)
  const canteenAction = ref(null)
  const year = Number(window.TELEDECLARATION_YEAR)
  const diagnosticErrors = ref([])
  const diagnoticCheck = ref({})
  const diagnosticRecap = ref(null)
  const hasDiagnostic = computed(() => diagnostic.value !== null)
  const hasErrors = computed(() => diagnosticErrors.value.length > 0)
  const isSimple = computed(() => diagnostic.value?.diagnosticType === "SIMPLE")
  const isComplete = computed(() => diagnostic.value?.diagnosticType === "COMPLETE")
  const isSaved = ref(true)
  const hasSelectAutofill = ref(false)
  const isTeledeclared = computed(() => diagnostic.value?.isTeledeclared)
  const visitedPagesSeparator = ","
  const tunnelApproVisitedPages = computed(() => diagnostic.value?.tunnelAppro?.split(visitedPagesSeparator) || [])

  /* Init store with diagnostic of the current campaign */
  async function initStore(canteenId) {
    if (canteenSavedId.value === Number(canteenId)) return
    const diagnosticsResponse = await diagnosticService.fetchDiagnostics(canteenId)
    if (diagnosticsResponse?.status === "error") useRootStore().notifyServerError(diagnosticsResponse)
    const diagnosticYear = diagnosticsResponse?.results?.find((result) => result.year === year) || null
    if (!diagnosticYear) deleteStore()
    else {
      setDiagnostic(diagnosticYear)
      setCanteenId(canteenId)
      await setCanteenAction()
      await checkDiagnosticSteps()
      await setDiagnosticRecap()
    }
  }

  /* Check diagnostic and canteen for the "volets" */
  async function checkDiagnosticSteps() {
    if (!diagnostic.value) return
    const canteenId = diagnostic.value.canteenId
    const diagnosticCheck = await diagnosticService.checkDiagnostic(canteenId, diagnostic.value.id)
    const canteenCheck = await canteenService.checkCanteen(canteenId)
    const check = {
      isClean: canteenCheck.isClean && diagnosticCheck.isClean,
      isFilled: canteenCheck.isFilled && diagnosticCheck.isFilled,
      errors: {...canteenCheck.errors, ...diagnosticCheck.errors}
    }
    addErrorsFromCheck(check.errors)
    diagnoticCheck.value = check
    return check
  }

  /* Fetch the recap of the diagnostic */
  async function setDiagnosticRecap() {
    if (!diagnostic.value) {
      diagnosticRecap.value = null
      return
    }
    const response = await diagnosticService.fetchDiagnosticRecap(diagnostic.value.canteenId, diagnostic.value.id)
    diagnosticRecap.value = response.status === "error" ? null : response
  }

  /* Teledeclare diagnostic */
  async function teledeclare() {
    if (!diagnostic.value) return
    const response = await diagnosticService.teledeclareDiagnostic(diagnostic.value.canteenId, diagnostic.value.id)
    if (response?.status === "error") return response
    setDiagnostic({ ...diagnostic.value, isTeledeclared: true })
    await setCanteenAction()
    await setDiagnosticRecap()
    return response
  }

  /* Cancel teledeclaration of the diagnostic */
  async function cancelTeledeclaration() {
    if (!diagnostic.value) return
    const response = await diagnosticService.cancelTeledeclaration(diagnostic.value.canteenId, diagnostic.value.id)
    if (response?.status === "error") return response
    setDiagnostic({ ...diagnostic.value, isTeledeclared: false })
    await setCanteenAction()
    await setDiagnosticRecap()
    return response
  }

  /* Save diagnostic */
  async function saveDiagnostic() {
    if (!diagnostic.value) return
    const canteenId = diagnostic.value.canteenId
    if (hasSelectAutofill.value && !diagnostic.value.generatedFromPurchases) autofillDiagnostic()
    const diagnosticValues = diagnostic.value
    const response = await diagnosticService.updateDiagnostic(canteenId, diagnosticValues.id, diagnosticValues)
    if (response.status === "error") replaceErrors(response.list)
    else setDiagnostic(response)
    await setCanteenAction()
    return response
  }

  /* Save only the given fields of the diagnostic */
  async function updateMealCount() {
    if (!diagnostic.value) return
    const canteenId = diagnostic.value.canteenId
    const valeurTotalFieldName = teledeclarationFields.getFieldsListFromGroup("valeurTotale")[0]
    const coutRepasFieldName = teledeclarationFields.getFieldsListFromGroup("coutRepas")[0]
    const response = await diagnosticService.updateDiagnostic(canteenId, diagnostic.value.id, { [valeurTotalFieldName]: diagnostic.value[valeurTotalFieldName] })
    if (response.status === "error") replaceErrors(response.list)
    else setValue(coutRepasFieldName, response[coutRepasFieldName])
    return response
  }

  /* Fill the diagnostic with the purchases values */
  function autofillDiagnostic() {
    const autofillSteps = ["egalim", "origine", "localCircuitCourt"]
    const purchaseSummary = useStorePurchaseSummary().purchaseSummary
    const fields = teledeclarationFields.getFieldsWithAutofill()
    for (const field of fields) setValue(field, purchaseSummary[field])
    setValue("generatedFromPurchases", true)
    autofillSteps.forEach((slug) => markPageAsVisited(slug))
  }

  /* Set if the diagnostic must be filled from purchases on next save */
  function setSelectAutofill(value) {
    hasSelectAutofill.value = value
  }

  /* Save the page slug in the list of the visited pages */
  function markPageAsVisited(slug) {
    if (!diagnostic.value || !slug || tunnelApproVisitedPages.value.includes(slug)) return
    diagnostic.value.tunnelAppro = [...tunnelApproVisitedPages.value, slug].join(visitedPagesSeparator)
  }

  /* Check if the step has been visited */
  function isPageVisited(slug) {
    return tunnelApproVisitedPages.value.includes(slug)
  }

  /* Only display errors if the step has been visited before */
  function getDisplayedErrors(slug) {
    if (!slug || isPageVisited(slug)) return diagnosticErrors.value
    return []
  }

  /* Set canteen id */
  function setCanteenId(canteenId) {
    canteenSavedId.value = Number(canteenId)
  }

  /* TO IMPROVE : Set the action to do by the canteen for the current campaign */
  async function setCanteenAction() {
    if (!canteenSavedId.value || !year) return
    const canteens = await canteenService.fetchCanteensActions(year)
    const canteen = canteens.find((canteen) => canteen.id === canteenSavedId.value)
    canteenAction.value = canteen?.action || null
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
    clearError(field)
  }

  /* Empty store */
  function deleteStore() {
    refreshStore()
    diagnostic.value = null
    canteenAction.value = null
    isSaved.value = true
    hasSelectAutofill.value = false
    diagnoticCheck.value = {}
    diagnosticRecap.value = null
    diagnosticErrors.value = []
  }

  /* Force refresh store on next init */
  function refreshStore() {
    canteenSavedId.value = null
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
    diagnoticCheck.value = {}
  }

  /* Clear one error */
  const clearError = (field) => {
    diagnosticErrors.value = diagnosticErrors.value.filter((error) => error.field !== field)
  }

  /* Keep only the errors related to the fields displayed on the given page */
  function getErrorsPage(pageName, canteenIsGroupe) {
    const fieldsList = teledeclarationFields.getFieldsListFromPage(pageName, canteenIsGroupe, isSimple.value)
    return diagnosticErrors.value.filter((error) => fieldsList.includes(error.field))
  }

  /* Keep only the errors related to the fields displayed on the given page */
  function getErrorsGroup(fieldsGroupName) {
    const fieldsList = teledeclarationFields.getFieldsListFromGroup(fieldsGroupName)
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
    canteenAction,
    diagnosticErrors,
    diagnoticCheck,
    diagnosticRecap,
    hasDiagnostic,
    hasErrors,
    isSimple,
    isComplete,
    isSaved,
    hasSelectAutofill,
    isTeledeclared,
    initStore,
    checkDiagnosticSteps,
    teledeclare,
    cancelTeledeclaration,
    deleteStore,
    refreshStore,
    getYear,
    setDiagnostic,
    setValue,
    saveDiagnostic,
    updateMealCount,
    autofillDiagnostic,
    setSelectAutofill,
    markPageAsVisited,
    isPageVisited,
    getDisplayedErrors,
    addErrorsFromCheck,
    clearErrors,
    getErrorsPage,
    getErrorsGroup,
    isFieldError,
    getErrorMessage,
  }
})

export { useStoreTeledeclaration }
