<template>
  <div>
    <p :class="{ 'my-0': true, inline: singleLine }" v-if="hasSatelliteCanteens">
      <v-icon small>$community-fill</v-icon>
      {{ canteen.satelliteCanteensCount }} satellites
    </p>
    <p :class="{ 'my-0': true, inline: singleLine }" v-if="hasDailyMealCount">
      <span class="mx-1" v-if="singleLine && hasSatelliteCanteens">/</span>
      <v-icon small>$restaurant-fill</v-icon>
      <!-- eslint-disable-next-line prettier/prettier-->
      {{ canteen.dailyMealCount }} par jour<span v-if="canteen.productionType === 'site_cooked_elsewhere'">, livrés</span>
    </p>
    <p :class="{ 'my-0': true, inline: singleLine }" v-if="canteen.city">
      <span class="mx-1" v-if="singleLine && (hasSatelliteCanteens || hasDailyMealCount)">/</span>
      <v-icon small aria-hidden="false" role="img" aria-label="Localisation">$compass-3-fill</v-icon>
      {{ canteen.city }}
    </p>
    <p :class="{ 'my-0': true, inline: singleLine }" v-if="types">
      <span class="mx-1" v-if="singleLine && (canteen.dailyMealCount || canteen.city)">/</span>
      <v-icon small aria-hidden="false" role="img" aria-label="Secteurs">$building-fill</v-icon>
      {{ types }}
    </p>
  </div>
</template>

<script>
import { capitalise } from "@/utils"

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
    useCategories: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    types() {
      if (!this.canteen.sectors) return null
      return this.useCategories ? this.categoriesDisplayString : this.sectorsDisplayString
    },
    categoriesDisplayString() {
      const categories = this.sectors.map((s) => s.category)
      const uniqueCategories = categories.filter((c, idx, self) => c && self.indexOf(c) === idx)
      return capitalise(uniqueCategories.join(", "))
    },
    sectorsDisplayString() {
      return capitalise(this.sectors.map((x) => x.name.toLowerCase()).join(", "))
    },
    sectors() {
      const sectors = this.$store.state.sectors
      return this.canteen.sectors.map((sectorId) => sectors.find((s) => s.id === sectorId))
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
