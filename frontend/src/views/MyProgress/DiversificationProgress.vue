<template>
  <div>
    Diversification Progress
    <div v-if="diagnostic">plan de diversification en place : {{ diagnostic.hasDiversificationPlan }}</div>
    <div v-else>Pas de diagnostic</div>
  </div>
</template>

<script>
export default {
  name: "DiversificationProgress",
  props: ["diagnostic"],
}
</script>
