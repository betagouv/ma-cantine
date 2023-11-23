<template>
  <div>
    <h1 class="fr-text font-weight-bold text-uppercase mb-4">Synthèse</h1>
    <component :is="componentName" :canteen="canteen" :diagnostic="diagnostic" />
  </div>
</template>

<script>
import WasteMeasureSummary from "@/components/DiagnosticSummary/WasteMeasureSummary"
import DiversificationMeasureSummary from "@/components/DiagnosticSummary/DiversificationMeasureSummary"
import InformationMeasureSummary from "@/components/DiagnosticSummary/InformationMeasureSummary"

export default {
  name: "SummaryWrapper",
  components: {
    WasteMeasureSummary,
    DiversificationMeasureSummary,
    InformationMeasureSummary,
  },
  props: {
    componentName: {
      type: String,
      required: true,
    },
    canteen: {
      type: Object,
      required: true,
    },
    diagnostic: {
      type: Object,
      required: true,
    },
  },
}
</script>
