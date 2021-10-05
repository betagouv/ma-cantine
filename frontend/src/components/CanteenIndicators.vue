<template>
  <div>
    <p class="my-0" v-if="includeProductOrigin && productOriginDiagnostic">
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
import { lastYear, getPercentage, isDiagnosticComplete } from "@/utils"

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
    productOriginDiagnostic() {
      const latestDiagnostic = this.canteen.diagnostics.find((x) => x.year === lastYear())
      if (!latestDiagnostic || !isDiagnosticComplete(latestDiagnostic)) return null
      return latestDiagnostic
    },
    productOriginText() {
      const bioPercent = getPercentage(
        this.productOriginDiagnostic.valueBioHt,
        this.productOriginDiagnostic.valueTotalHt
      )
      const sustainablePercent = getPercentage(
        this.productOriginDiagnostic.valueSustainableHt,
        this.productOriginDiagnostic.valueTotalHt
      )
      return `${bioPercent} % bio, ${sustainablePercent} % qualité et durables`
    },
  },
}
</script>
