<template>
  <div class="summary px-4 py-10">
    <h1 class="fr-text font-weight-bold text-uppercase mb-4">Synthèse</h1>
    <component :is="`${measure.baseComponent}Summary`" :canteen="canteen" :diagnostic="diagnostic" />
  </div>
</template>

<script>
import QualityMeasureSummary from "@/components/DiagnosticSummary/QualityMeasureSummary"
import WasteMeasureSummary from "@/components/DiagnosticSummary/WasteMeasureSummary"
import DiversificationMeasureSummary from "@/components/DiagnosticSummary/DiversificationMeasureSummary"
import NoPlasticMeasureSummary from "@/components/DiagnosticSummary/NoPlasticMeasureSummary"
import InformationMeasureSummary from "@/components/DiagnosticSummary/InformationMeasureSummary"

export default {
  name: "SummaryWrapper",
  components: {
    QualityMeasureSummary,
    WasteMeasureSummary,
    DiversificationMeasureSummary,
    NoPlasticMeasureSummary,
    InformationMeasureSummary,
  },
  props: {
    measure: {
      type: Object,
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

<style>
.summary {
  height: 100%;
  background: #fff;
  border: 1px solid #ddd;
}
</style>
