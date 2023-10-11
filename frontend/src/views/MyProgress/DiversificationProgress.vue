<template>
  <div>
    Diversification Progress
    <div v-if="usesCentralDiagnostic">Vos données sont fournis par votre cuisine centrale</div>
    <div v-else-if="usesSatelliteDiagnostic">Vos satellites fournis ces données eux-mêmes</div>
    <div v-else-if="diagnostic">plan de diversification en place : {{ diagnostic.hasDiversificationPlan }}</div>
    <div v-else>Pas de diagnostic</div>
  </div>
</template>

<script>
export default {
  name: "DiversificationProgress",
  props: ["diagnostic", "centralDiagnostic"],
  computed: {
    usesCentralDiagnostic() {
      return this.centralDiagnostic?.centralKitchenDiagnosticMode === "ALL"
    },
    usesSatelliteDiagnostic() {
      return this.diagnostic?.centralKitchenDiagnosticMode === "APPRO"
    },
  },
}
</script>
