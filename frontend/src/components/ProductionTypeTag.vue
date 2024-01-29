<template>
  <div v-if="canteen.isCentralCuisine || isSatellite">
    <div class="tag px-2">
      <p v-if="canteen.isCentralCuisine" class="mb-0 fr-text-xs">
        <v-icon class="mt-n1 grey--text text--darken-4" small>$community-fill</v-icon>
        Cuisine centrale
      </p>
      <p v-else-if="isSatellite" class="mb-0 fr-text-xs">
        <v-icon class="mt-n1 grey--text text--darken-4" small>$restaurant-fill</v-icon>
        Cantine satellite
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProductionTypeTag",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  computed: {
    isSatellite() {
      const productionType = this.canteen?.productionType
      return productionType === "site_cooked_elsewhere"
    },
  },
}
</script>

<style scoped>
.tag {
  --text-spacing: 0;
  --title-spacing: 0;
  --underline-img: none;
  /* --hover-tint: var(--hover); */
  --hover-tint: #f6f6f6;
  --idle: transparent;
  /* --hover: var(--background-contrast-grey-hover);
  --active: var(--background-contrast-grey-active); */
  --hover: #d2d2d2;
  --active: #c1c1c1;
  align-items: center;
  background-color: #eee;
  /* background-color: var(--background-contrast-grey); */
  border-radius: 1rem;
  color: #161616;
  /* color: var(--text-label-grey); */
  display: inline-flex;
  flex-direction: row;
  font-size: 0.875rem;
  justify-content: center;
  line-height: 1.5rem;
  min-height: 2rem;
  min-width: 2.25rem;
  padding: 0.25rem 0.75rem;
  width: -moz-fit-content;
  width: fit-content;
}
</style>
