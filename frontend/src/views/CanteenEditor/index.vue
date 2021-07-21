<template>
  <div class="mt-n2">
    <v-row class="mt-2">
      <v-col cols="12" sm="4" md="3">
        <CanteenNavigation :canteen="canteen" />
      </v-col>
      <v-col>
        <router-view :key="$route.fullPath" :originalCanteen="canteen"></router-view>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import CanteenNavigation from "@/components/CanteenNavigation"

export default {
  name: "CanteenEditor",
  components: { CanteenNavigation },
  props: {
    canteenUrlComponent: {
      type: String,
      required: false,
    },
  },
  computed: {
    canteen() {
      return this.canteenUrlComponent && this.$store.getters.getCanteenFromUrlComponent(this.canteenUrlComponent)
    },
  },
}
</script>
