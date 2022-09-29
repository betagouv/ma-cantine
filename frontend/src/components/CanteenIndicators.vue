<template>
  <div>
    <p class="my-0" :class="{ inline: singleLine }" v-if="hasSatelliteCanteens">
      <span class="icon i-community"></span>
      {{ canteen.satelliteCanteensCount }} satellites
    </p>
    <p class="my-0" :class="{ inline: singleLine }" v-if="hasDailyMealCount">
      <span class="mx-1" v-if="singleLine && hasSatelliteCanteens">/</span>
      <span class="icon i-restaurant">Repas :</span>
      <!-- eslint-disable-next-line prettier/prettier-->
      {{ canteen.dailyMealCount }} par jour
      <span v-if="canteen.productionType === 'site_cooked_elsewhere'">, livrés</span>
    </p>
    <p class="my-0" :class="{ inline: singleLine }" v-if="canteen.city">
      <span class="mx-1" v-if="singleLine && (hasSatelliteCanteens || hasDailyMealCount)">/</span>
      <span class="icon i-compass">Ville :</span>
      {{ canteen.city }}
    </p>
    <p class="my-0" :class="{ inline: singleLine }" v-if="sectors">
      <span class="mx-1" v-if="singleLine && (hasSatelliteCanteens || canteen.dailyMealCount || canteen.city)">/</span>
      <span class="icon i-building">Secteurs d'activité :</span>
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
.icon,
.icon::before {
  --icon-size: var(--icon-small);
  --font-size: var(--icon-small-font);
}
span.icon::before {
  background-color: #777;
}
.i-community::before {
  --icon-image: url("/static/icons/community-fill.svg");
}
.i-compass::before {
  --icon-image: url("/static/icons/compass-3-fill.svg");
}
.i-building::before {
  --icon-image: url("/static/icons/building-fill.svg");
}
</style>
