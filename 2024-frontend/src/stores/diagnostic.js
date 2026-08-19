import { defineStore } from "pinia"
import { computed, ref } from "vue"
import diagnosticService from "@/services/diagnostics.js"

const useStoreDiagnostic = defineStore("diagnostic", () => {
  const diagnostics = ref({})
  const lastYear = new Date().getFullYear() - 1

  /* Diagnostic of the current campaign */
  const diagnosticCurrentCampaign = computed(() => diagnostics.value[lastYear])

  /* Init store with diagnostics of all the years */
  async function initStore(canteenId) {
    const response = await diagnosticService.fetchDiagnostics(canteenId)
    for (let i = 0; i < response["results"].length; i++) {
      const resultYear = response["results"][i].year
      diagnostics.value[resultYear] = response["results"][i]
    }
  }

  /* Update diagnostic of the current campaign */
  function updateDiagnosticCurrentCampaign(diagnostic) {
    diagnostics.value[lastYear] = diagnostic
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
  }
})

export { useStoreDiagnostic }
