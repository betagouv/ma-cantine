<script setup>
import WasteMeasurementSummary from "@/components/WasteMeasurementSummary.vue"

defineProps(["measurement"])
</script>

<template>
  <div class="summary fr-p-5w">
    <h1 class="fr-h2 fr-mb-4w">Mes déchets alimentaires mesurés</h1>
    <WasteMeasurementSummary :measurement="measurement" />
  </div>
</template>

<style scoped>
.summary {
  height: 100%;
  overflow: scroll;
  background: #fff;
  border: 1px solid #ddd;
}
</style>
