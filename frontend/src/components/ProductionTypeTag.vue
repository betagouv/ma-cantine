<template>
  <p v-if="isCentralKitchen || isSatellite" :class="`tag fr-text-xs mb-0 ${position}`">
    <v-icon x-small>{{ isCentralKitchen ? "$community-fill" : "$restaurant-fill" }}</v-icon>
    {{ isCentralKitchen ? "Cuisine centrale" : "Cantine satellite" }}
  </p>
</template>

<script>
export default {
  name: "ProductionTypeTag",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
    position: {
      type: String,
      default: "",
    },
  },
  computed: {
    isCentralKitchen() {
      return this.canteen.isCentralCuisine
    },
    isSatellite() {
      return this.canteen.isSatellite
    },
  },
}
</script>

<style scoped>
.tag {
  display: flex;
  padding: 2px 8px;
  justify-content: center;
  align-items: center;
  gap: 2px;
  border-radius: 12px;
  background-color: #eee;
  color: #161616;
  width: fit-content;
}
.tag .v-icon {
  color: #161616;
}
.tag.top-left {
  position: absolute;
  left: 12px;
  top: 12px;
}
</style>
