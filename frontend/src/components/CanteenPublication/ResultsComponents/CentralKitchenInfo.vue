<template>
  <!-- TODO: use DsfrCallout instead -->
  <v-card outlined elevation="0" color="primary lighten-5" class="d-flex mb-6">
    <v-icon class="ml-4" color="primary">$information-fill</v-icon>

    <v-card-text>
      <p class="mb-0">
        La cantine « {{ canteen.name }} » sert des repas cuisinés dans la cuisine centrale
        <span v-if="centralKitchen.publicationStatus === 'published'">
          <router-link
            :to="{
              name: 'CanteenPage',
              params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(centralKitchen) },
            }"
          >
            « {{ centralKitchen.name }} »
          </router-link>
          .
        </span>
        <span v-else>« {{ centralKitchen.name }} ».</span>
        Les valeurs ci-dessous sont celles du lieu de production des repas.
      </p>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "CentralKitchenInfo",
  props: {
    canteen: Object,
  },
  computed: {
    centralKitchen() {
      return this.canteen.centralKitchen
    },
  },
}
</script>
