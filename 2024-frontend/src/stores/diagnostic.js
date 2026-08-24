import { defineStore } from "pinia"
import { computed, ref } from "vue"
import diagnosticService from "@/services/diagnostics.js"

const useStoreDiagnostic = defineStore("diagnostic", () => {
  const diagnostics = ref({})
  const lastYear = new Date().getFullYear() - 1
  const diagnosticCurrentCampaign = computed(() => diagnostics.value[lastYear])

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
    if (response.status !== "error") updateDiagnosticCurrentCampaign(response)
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

  return {
    diagnostics,
    diagnosticCurrentCampaign,
    initStore,
    deleteStore,
    hasDiagnosticCurrentCampaign,
    updateDiagnosticCurrentCampaign,
    setDiagnosticCurrentCampaign,
    saveDiagnosticCurrentCampaign,
  }
})

export { useStoreDiagnostic }
