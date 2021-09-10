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
      <CanteenIndicators :canteen="canteen" />
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
import CanteenIndicators from "@/components/CanteenIndicators"
import { lastCompleteYear } from "@/utils"

export default {
  name: "PublishedCanteenCard",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  components: {
    CanteenIndicators,
  },
  methods: {
    initiativesForCanteen(canteen) {
      if (!canteen.diagnostics || canteen.diagnostics.length === 0) return null

      const diagnostic = canteen.diagnostics.find((x) => x.year === lastCompleteYear())
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
