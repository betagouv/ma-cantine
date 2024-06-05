<template>
  <div :class="{ 'fr-text grey--text text--darken-2': true, 'd-flex flex-wrap': singleLine }">
    <p :class="{ 'my-0 d-flex align-center': true, 'inline mr-3': singleLine }" v-if="canteen.city">
      <v-icon small class="mr-1">$map-pin-2-line</v-icon>
      {{ canteen.city }}
    </p>
    <p :class="{ 'my-0 d-flex align-center': true, 'inline mr-3': singleLine }" v-if="hasDailyMealCount">
      <v-icon small class="mr-1" aria-hidden="false" role="img">$restaurant-line</v-icon>
      <!-- eslint-disable-next-line prettier/prettier-->
      {{ canteen.dailyMealCount }} couverts<span v-if="canteen.productionType === 'site_cooked_elsewhere'">, livrés</span>
    </p>
    <p :class="{ 'my-0 d-flex align-center': true, 'inline mr-3': singleLine }" v-if="hasSatelliteCanteens">
      <v-icon small class="mr-1">$community-line</v-icon>
      {{ canteen.satelliteCanteensCount }} satellites
    </p>
    <p :class="{ 'my-0 d-flex align-center': true, 'inline mr-3': singleLine }" v-if="businessSegments">
      <v-icon small class="mr-1">$building-line</v-icon>
      {{ businessSegments }}
    </p>
  </div>
</template>

<script>
import { capitalise } from "@/utils"
import Constants from "@/constants"

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
    businessSegments() {
      if (!this.canteen.sectors) return null
      return this.useCategories ? this.categoriesDisplayString : this.sectorsDisplayString
    },
    categoriesDisplayString() {
      const categories = this.sectors.map((s) => s.category)
      const uniqueCategories = categories.filter((c, idx, self) => c && self.indexOf(c) === idx)
      return capitalise(uniqueCategories.map((c) => Constants.SectorCategoryTranslations[c]).join(", "))
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
