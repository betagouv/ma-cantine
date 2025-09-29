<template>
  <div
    :class="{
      'grey--text text--darken-2': true,
      'd-flex flex-wrap': singleLine,
      'fr-text': !dense,
      'fr-text-xs': dense,
    }"
  >
    <p :class="{ 'my-0 d-flex align-center': true, 'inline mr-3': singleLine }" v-if="canteen.city">
      <v-icon :small="!dense" :x-small="dense" class="mr-1">$map-pin-2-line</v-icon>
      {{ canteen.city }}
    </p>
    <p :class="{ 'my-0 d-flex align-center': true, 'inline mr-3': singleLine }" v-if="hasDailyMealCount">
      <v-icon :small="!dense" :x-small="dense" class="mr-1" aria-hidden="false" role="img">$team-line</v-icon>
      {{ canteen.dailyMealCount }} couverts
    </p>
    <p :class="{ 'my-0 d-flex align-center': true, 'inline mr-3': singleLine }" v-if="satelliteCount">
      <v-icon :small="!dense" :x-small="dense" class="mr-1">$restaurant-line</v-icon>
      {{ satelliteCount }} {{ satelliteCount === 1 ? "restaurant satellite" : "restaurants satellites" }}
    </p>
    <p :class="{ 'my-0 d-flex align-center': true, 'inline mr-3': singleLine }" v-if="businessSegments">
      <v-icon :small="!dense" :x-small="dense" class="mr-1">$building-line</v-icon>
      {{ businessSegments }}
    </p>
    <p :class="{ 'my-0 d-flex align-center': true, 'inline mr-3': singleLine }" v-if="managementType">
      <v-icon :small="!dense" :x-small="dense" class="mr-1">$group-line</v-icon>
      Gestion {{ managementType.toLowerCase() }}
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
    dense: {
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
    satelliteCount() {
      return this.canteen.isCentralCuisine ? this.canteen.satelliteCanteensCount : undefined
    },
    hasDailyMealCount() {
      return this.canteen.dailyMealCount
    },
    managementType() {
      return Constants.ManagementTypes.find((type) => type.value === this.canteen.managementType)?.text
    },
  },
}
</script>

<style scoped>
.inline {
  display: inline;
}
</style>
