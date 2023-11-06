<template>
  <component :is="step.componentName" :canteen="canteen" :diagnostic="diagnostic" v-on:update-payload="updatePayload" />
</template>

<script>
import WasteMeasureSummary from "@/components/DiagnosticSummary/WasteMeasureSummary"

export default {
  name: "WasteSteps",
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
    WasteMeasureSummary,
  },
  data() {
    return {
      steps: [
        {
          title: "Synthèse",
          isSynthesis: true,
          componentName: "WasteMeasureSummary",
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
    this.$emit("update-steps", this.steps)
  },
}
</script>
