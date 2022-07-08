<template>
  <div>
    <p :class="{ 'my-0': true, inline: singleLine }" v-if="hasSatelliteCanteens">
      <span v-if="hasSatelliteCanteens" class="mr-1">
        <v-icon small>mdi-home-city</v-icon>
        {{ canteen.satelliteCanteensCount }} satellites
      </span>
    </p>
    <p :class="{ 'my-0': true, inline: singleLine }" v-if="hasDailyMealCount">
      <span class="mx-1" v-if="singleLine && hasSatelliteCanteens">/</span>
      <span>
        <v-icon small>mdi-silverware-fork-knife</v-icon>
        <!-- eslint-disable-next-line prettier/prettier-->
        {{ canteen.dailyMealCount }} par jour<span v-if="canteen.productionType === 'site_cooked_elsewhere'">, livrés</span>
      </span>
    </p>
    <p :class="{ 'my-0': true, inline: singleLine }" v-if="canteen.city">
      <span class="mx-1" v-if="singleLine && (hasSatelliteCanteens || hasDailyMealCount)">/</span>
      <v-icon small aria-hidden="false" role="img" aria-label="Localisation">mdi-compass</v-icon>
      {{ canteen.city }}
    </p>
    <p :class="{ 'my-0': true, inline: singleLine }" v-if="sectors">
      <span class="mx-1" v-if="singleLine && (canteen.dailyMealCount || canteen.city)">/</span>
      <v-icon small aria-hidden="false" role="img" aria-label="Secteurs">mdi-office-building</v-icon>
      {{ sectors }}
    </p>
  </div>
</template>

<script>
export default {
  name: "CanteenIndicators",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
    singleLine: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    sectors() {
      if (!this.canteen.sectors) return null
      const sectors = this.$store.state.sectors
      const sectorDisplay = this.canteen.sectors
        .map((sectorId) => sectors.find((x) => x.id === sectorId).name.toLowerCase())
        .join(", ")
      return sectorDisplay.charAt(0).toUpperCase() + sectorDisplay.slice(1)
    },
    hasSatelliteCanteens() {
      return (
        this.canteen.satelliteCanteensCount &&
        (this.canteen.productionType === "central" || this.canteen.productionType === "central_serving")
      )
    },
    hasDailyMealCount() {
      return this.canteen.dailyMealCount && this.canteen.productionType !== "central"
    },
  },
}
</script>

<style scoped>
.inline {
  display: inline;
}
</style>
