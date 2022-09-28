<template>
  <div>
    <p class="my-0 satellite-count" :class="{ inline: singleLine }" v-if="hasSatelliteCanteens">
      {{ canteen.satelliteCanteensCount }} satellites
    </p>
    <span class="mx-1" v-if="singleLine && hasDailyMealCount && hasSatelliteCanteens">/</span>
    <p class="my-0 meal-count" :class="{ inline: singleLine }" v-if="hasDailyMealCount">
      <!-- eslint-disable-next-line prettier/prettier-->
      {{ canteen.dailyMealCount }} par jour<span v-if="canteen.productionType === 'site_cooked_elsewhere'">, livrés</span>
    </p>
    <span class="mx-1" v-if="singleLine && canteen.city && (hasSatelliteCanteens || hasDailyMealCount)">/</span>
    <p class="my-0 location" :class="{ inline: singleLine }" v-if="canteen.city">
      {{ canteen.city }}
    </p>
    <span class="mx-1" v-if="singleLine && sectors && (canteen.dailyMealCount || canteen.city)">/</span>
    <p class="my-0 sectors" :class="{ inline: singleLine }" v-if="sectors">
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
p::before {
  --icon-size: 1.2rem;
  content: "";
  display: inline-block;
  flex: 0 0 auto;
  height: var(--icon-size);
  width: var(--icon-size);
  background-color: #777;
  vertical-align: calc(0.375em - var(--icon-size) * 0.5);
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
