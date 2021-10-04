<template>
  <div>
    <p class="my-0" v-if="includeProductOrigin && latestDiagnostic">
      <v-icon small>mdi-food-apple</v-icon>
      {{ productOriginText }}
    </p>
    <p class="my-0" v-if="canteen.dailyMealCount">
      <v-icon small>mdi-silverware-fork-knife</v-icon>
      {{ canteen.dailyMealCount }} repas par jour
    </p>
    <p class="my-0" v-if="canteen.city">
      <v-icon small aria-hidden="false" role="img" aria-label="Localisation">mdi-compass</v-icon>
      {{ canteen.city }}
    </p>
    <p class="my-0" v-if="sectors">
      <v-icon small aria-hidden="false" role="img" aria-label="Secteurs">mdi-office-building</v-icon>
      {{ sectors }}
    </p>
  </div>
</template>

<script>
import { lastYear, getPercentage } from "@/utils"

export default {
  name: "CanteenIndicators",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
    includeProductOrigin: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    sectors() {
      if (!this.canteen.sectors) return null
      const sectors = this.$store.state.sectors
      return this.canteen.sectors
        .map((sectorId) => sectors.find((x) => x.id === sectorId).name.toLowerCase())
        .join(", ")
    },
    latestDiagnostic() {
      return this.canteen.diagnostics.find((x) => x.year === lastYear())
    },
    productOriginText() {
      const bioPercent = getPercentage(this.latestDiagnostic.valueBioHt, this.latestDiagnostic.valueTotalHt)
      const sustainablePercent = getPercentage(
        this.latestDiagnostic.valueSustainableHt,
        this.latestDiagnostic.valueTotalHt
      )
      return `${bioPercent} % bio, ${sustainablePercent} % qualité et durables`
    },
  },
}
</script>
