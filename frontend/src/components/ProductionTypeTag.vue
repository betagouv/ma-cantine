<template>
  <DsfrTag
    :clickable="false"
    v-if="isGroupe || isSatellite"
    :class="`${position}`"
    :icon="isGroupe ? '$community-fill' : '$restaurant-fill'"
    :text="isGroupe ? 'Groupe de restaurants satellites' : 'Restaurant satellite'"
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
    isGroupe() {
      return this.canteen.productionType === "groupe"
    },
    isSatellite() {
      return this.canteen.isSatellite
    },
  },
}
</script>
