<template>
  <component :is="step.componentName" :canteen="canteen" :diagnostic="diagnostic" v-on:update-payload="updatePayload" />
</template>

<script>
import QualityMeasureSummary from "@/components/DiagnosticSummary/QualityMeasureSummary"
import QualityTotalStep from "./QualityTotalStep"

export default {
  name: "QualitySteps",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
    diagnostic: {
      type: Object,
      required: true,
    },
    stepUrlSlug: {
      type: String,
    },
  },
  components: {
    QualityTotalStep,
    QualityMeasureSummary,
  },
  data() {
    return {
      steps: [
        {
          title: "Valeurs totales des achats alimentaires",
          componentName: "QualityTotalStep",
          urlSlug: "total",
        },
        {
          title: "Synthèse",
          isSynthesis: true,
          componentName: "QualityMeasureSummary",
          urlSlug: "synthèse",
        },
      ],
    }
  },
  computed: {
    step() {
      const step = this.stepUrlSlug && this.steps.find((step) => step.urlSlug === this.stepUrlSlug)
      return step || this.steps[0]
    },
  },
  methods: {
    updatePayload(data) {
      this.$emit("update-payload", data)
    },
  },
  mounted() {
    this.$emit("updateSteps", this.steps)
  },
}
</script>
