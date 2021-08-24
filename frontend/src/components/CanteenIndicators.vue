<template>
  <div>
    <div v-if="canteen.dailyMealCount">
      <v-icon small>mdi-silverware-fork-knife</v-icon>
      {{ canteen.dailyMealCount }} repas par jour
    </div>
    <div v-if="canteen.city">
      <v-icon small>mdi-compass</v-icon>
      {{ canteen.city }}
    </div>
    <div v-if="sectors">
      <v-icon small>mdi-office-building</v-icon>
      {{ sectors }}
    </div>
  </div>
</template>

<script>
export default {
  name: "CanteenIndicators",
  props: {
    canteen: {
      type: Object,
    },
  },
  computed: {
    sectors() {
      if (!this.canteen || !this.canteen.sectors) return null
      const sectors = this.$store.state.sectors
      return this.canteen.sectors
        .map((sectorId) => sectors.find((x) => x.id === sectorId).name.toLowerCase())
        .join(", ")
    },
  },
}
</script>
