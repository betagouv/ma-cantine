import { defineStore } from "pinia"
import { computed, ref } from "vue"
import diagnosticService from "@/services/diagnostics.js"

const useStoreDiagnostic = defineStore("diagnostic", () => {
  const diagnostics = ref({})
  const lastYear = new Date().getFullYear() - 1
  const diagnosticCurrentCampaign = computed(() => diagnostics.value[lastYear])
  const diagnosticCurrentCampaignErrors = ref([])

  /* Init store with diagnostics of all the years */
  async function initStore(canteenId) {
    const response = await diagnosticService.fetchDiagnostics(canteenId)
    for (let i = 0; i < response["results"].length; i++) {
      const resultYear = response["results"][i].year
      diagnostics.value[resultYear] = response["results"][i]
    }
  }

  /* Save diagnostic of the current campaign */
  async function saveDiagnosticCurrentCampaign() {
    const diagnostic = diagnosticCurrentCampaign.value
    if (!diagnostic) return
    const response = await diagnosticService.updateDiagnostic(diagnostic.canteenId, diagnostic.id, diagnostic)
    const errors = response?.list || []
    const hasErrors = errors.length > 0
    const isFieldError = errors.every(error => error.field !== null)
    if (response.status !== "error") updateDiagnosticCurrentCampaign(response)
    else if (hasErrors && isFieldError) saveDiagnosticCurrentCampaignErrors(response.list)
    return response
  }

  /* Update diagnostic of the current campaign */
  function updateDiagnosticCurrentCampaign(diagnostic) {
    diagnostics.value[lastYear] = diagnostic
  }

  /* Set value for diagnostic of the current campaign */
  function setDiagnosticCurrentCampaign(field, value) {
    diagnostics.value[lastYear][field] = value
  }

  /* Empty store */
  function deleteStore() {
    diagnostics.value = {}
  }

  /* Check if has diagnostic for the current campaign */
  function hasDiagnosticCurrentCampaign() {
    return diagnosticCurrentCampaign.value !== undefined
  }

  /* Save diagnostic errors for the current campaign */
  function saveDiagnosticCurrentCampaignErrors(errors) {
    diagnosticCurrentCampaignErrors.value = errors
  }

  /* Clear diagnostic errors for the current campaign */
  const clearDiagnosticCurrentCampaignErrors = () => {
    diagnosticCurrentCampaignErrors.value = []
  }

  return {
    diagnostics,
    diagnosticCurrentCampaign,
    diagnosticCurrentCampaignErrors,
    initStore,
    deleteStore,
    hasDiagnosticCurrentCampaign,
    updateDiagnosticCurrentCampaign,
    setDiagnosticCurrentCampaign,
    saveDiagnosticCurrentCampaign,
    saveDiagnosticCurrentCampaignErrors,
    clearDiagnosticCurrentCampaignErrors,
  }
})

export { useStoreDiagnostic }
