<template>
  <div>
    <p class="my-0 satellite-count" :class="{ inline: singleLine }" v-if="hasSatelliteCanteens">
      {{ canteen.satelliteCanteensCount }} satellites
    </p>
    <p class="my-0" :class="{ inline: singleLine }" v-if="hasDailyMealCount">
      <span class="mx-1" v-if="singleLine && hasSatelliteCanteens">/</span>
      <span class="icon-hint meal-count">Repas :</span>
      <!-- eslint-disable-next-line prettier/prettier-->
      {{ canteen.dailyMealCount }} par jour<span v-if="canteen.productionType === 'site_cooked_elsewhere'">, livrés</span>
    </p>
    <p class="my-0" :class="{ inline: singleLine }" v-if="canteen.city">
      <span class="mx-1" v-if="singleLine && (hasSatelliteCanteens || hasDailyMealCount)">/</span>
      <span class="icon-hint location">Ville :</span>
      {{ canteen.city }}
    </p>
    <p class="my-0" :class="{ inline: singleLine }" v-if="sectors">
      <span class="mx-1" v-if="singleLine && (hasSatelliteCanteens || canteen.dailyMealCount || canteen.city)">/</span>
      <span class="icon-hint sectors">Secteurs d'activité :</span>
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
.icon-hint {
  --icon-size: 1.1rem;
  height: var(--icon-size);
  width: var(--icon-size);
  overflow: hidden;
  display: inline-block;
  vertical-align: calc(0.435em - var(--icon-size) * 0.5);
}
.icon-hint::before {
  --icon-size: 1.1rem;
  content: "";
  display: inline-block;
  flex: 0 0 auto;
  height: var(--icon-size);
  width: var(--icon-size);
  background-color: #777;
  vertical-align: calc(0.435em - var(--icon-size) * 0.5);
}
.satellite-count::before {
  -webkit-mask-image: url("/static/icons/community-fill.svg");
  mask-image: url("/static/icons/community-fill.svg");
}
.meal-count::before {
  -webkit-mask-image: url("/static/icons/restaurant-fill.svg");
  mask-image: url("/static/icons/restaurant-fill.svg");
}
.location::before {
  -webkit-mask-image: url("/static/icons/compass-3-fill.svg");
  mask-image: url("/static/icons/compass-3-fill.svg");
}
.sectors::before {
  -webkit-mask-image: url("/static/icons/building-fill.svg");
  mask-image: url("/static/icons/building-fill.svg");
}
</style>
