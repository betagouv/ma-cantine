<template>
  <DsfrTag
    :clickable="false"
    v-if="isCentralKitchen || isSatellite"
    :class="`${position}`"
    :icon="isCentralKitchen ? '$community-fill' : '$restaurant-fill'"
    :text="isCentralKitchen ? 'Livreur des repas' : 'Restaurant satellite'"
  />
</template>

<script>
import DsfrTag from "@/components/DsfrTag"
export default {
  name: "ProductionTypeTag",
  components: { DsfrTag },
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
