<template>
  <v-card
    :to="{
      name: 'CanteenModification',
      params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
    }"
  >
    <v-img :src="canteen.mainImage || '/static/images/canteen-default-image.jpg'" height="160"></v-img>
    <v-card-title class="font-weight-bold">{{ canteen.name }}</v-card-title>
    <v-card-subtitle class="py-1">
      <v-chip small :color="canteen.dataIsPublic ? 'green lighten-4' : 'grey lighten-4'" label>
        {{ canteen.dataIsPublic ? "Publiée" : "Pas encore publiée" }}
      </v-chip>
    </v-card-subtitle>
    <v-card-subtitle v-if="canteen.dailyMealCount || canteen.city || canteen.sectors" class="mt-0">
      <div v-if="canteen.dailyMealCount">
        <v-icon small>mdi-silverware-fork-knife</v-icon>
        {{ canteen.dailyMealCount }} repas par jour
      </div>
      <div v-if="canteen.city">
        <v-icon small>mdi-compass</v-icon>
        {{ canteen.city }}
      </div>
      <div v-if="canteen.sectors.length">
        <v-icon small>mdi-office-building</v-icon>
        {{ sectors }}
      </div>
    </v-card-subtitle>
  </v-card>
</template>

<script>
export default {
  name: "CanteenCard",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  computed: {
    sectors() {
      const sectors = this.$store.state.sectors
      return this.canteen.sectors
        .map((sectorId) => sectors.find((x) => x.id === sectorId).name.toLowerCase())
        .join(", ")
    },
  },
}
</script>
