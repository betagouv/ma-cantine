<template>
  <div>
    <p v-if="badge.earned">{{ badge.subtitle }}</p>
    <p v-else>Cet établissement ne respecte pas encore la loi EGAlim pour cette mesure.</p>

    <component :is="`${badge.baseComponent}Summary`" :canteen="canteen" :diagnostic="diagnostic" />
  </div>
</template>

<script>
import { latestCreatedDiagnostic } from "@/utils"

import DiversificationMeasureSummary from "@/components/DiagnosticSummary/DiversificationMeasureSummary"
import InformationMeasureSummary from "@/components/DiagnosticSummary/InformationMeasureSummary"
import NoPlasticMeasureSummary from "@/components/DiagnosticSummary/NoPlasticMeasureSummary"
import WasteMeasureSummary from "@/components/DiagnosticSummary/WasteMeasureSummary"

export default {
  name: "GenericMeasureResults",
  props: {
    badge: Object,
    canteen: Object,
    diagnosticSet: Array,
  },
  components: {
    DiversificationMeasureSummary,
    InformationMeasureSummary,
    NoPlasticMeasureSummary,
    WasteMeasureSummary,
  },
  computed: {
    diagnostic() {
      return latestCreatedDiagnostic(this.diagnosticSet)
    },
  },
}
</script>
