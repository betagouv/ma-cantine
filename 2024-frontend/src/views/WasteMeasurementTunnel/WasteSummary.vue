<script setup>
import WasteMeasurementSummary from "@/components/WasteMeasurementSummary.vue"

defineProps(["measurement"])
</script>

<template>
  <div class="summary fr-p-5w">
    <h1 class="fr-text--md fr-mb-4w">Synthèse</h1>
    <WasteMeasurementSummary :measurement="measurement" />
  </div>
</template>

<style scoped>
h1 {
  font-weight: bold;
  text-transform: uppercase;
}
.summary {
  height: 100%;
  background: #fff;
  border: 1px solid #ddd;
}
</style>
