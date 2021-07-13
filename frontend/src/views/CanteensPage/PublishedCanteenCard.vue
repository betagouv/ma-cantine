<template>
  <v-card
    :to="{ name: 'CanteenPage', params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) } }"
    hover
    class="pa-4 text-left fill-height"
  >
    <v-card-title class="font-weight-black">
      {{ canteen.name }}
    </v-card-title>
    <v-card-subtitle v-if="canteen.dailyMealCount || canteen.city">
      <div v-if="canteen.dailyMealCount">
        <v-icon small>mdi-silverware-fork-knife</v-icon>
        {{ canteen.dailyMealCount }} repas par jour
      </div>
      <div v-if="canteen.city">
        <v-icon small>mdi-compass</v-icon>
        {{ canteen.city }}
      </div>
      <div v-if="sectorsForCanteen(canteen)">
        <v-icon small>mdi-office-building</v-icon>
        {{ sectorsForCanteen(canteen) }}
      </div>
    </v-card-subtitle>
    <v-card-text
      v-if="initiativesForCanteen(canteen) && initiativesForCanteen(canteen).length > 0"
      class="grey--text text--darken-4"
    >
      Nos initiatives mises en place :
      <div v-for="initiative in initiativesForCanteen(canteen)" :key="initiative">
        <v-icon small class="mt-n1" color="primary">mdi-check-bold</v-icon>
        {{ initiative }}
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "PublishedCanteenCard",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  methods: {
    sectorsForCanteen(canteen) {
      const sectors = canteen.sectors.map((x) => this.$store.state.sectors.find((y) => y.id === x)).filter((x) => !!x)

      if (sectors.length === 0) return null
      return sectors.map((x) => x.name.toLowerCase()).join(", ")
    },
    initiativesForCanteen(canteen) {
      if (!canteen.diagnostics || canteen.diagnostics.length === 0) return null

      const diagnostic = canteen.diagnostics.find((x) => x.year === 2020)
      if (!diagnostic) return null

      const initiatives = []
      if (diagnostic.hasDonationAgreement) initiatives.push("Dons faits aux associations")
      if (diagnostic.hasDiversificationPlan)
        initiatives.push("Mise en place d'un plan de diversification des protéines")
      if (diagnostic.cookingPlasticSubstituted || diagnostic.servingPlasticSubstituted)
        initiatives.push("Contenants en plastique remplacés")
      if (diagnostic.communicatesOnFoodPlan) initiatives.push("Communique sur le plan alimentaire")
      return initiatives
    },
  },
}
</script>
