<template>
  <div>
    <v-card elevation="0" class="text-center text-md-left mb-14 mt-6">
      <v-row v-if="$vuetify.breakpoint.smAndDown">
        <v-col cols="12">
          <v-img max-height="100px" contain src="/static/images/desktop.svg"></v-img>
        </v-col>
      </v-row>
      <v-row>
        <v-spacer></v-spacer>
        <v-col cols="3" v-if="$vuetify.breakpoint.mdAndUp">
          <div class="d-flex fill-height align-center">
            <v-img max-height="120px" contain src="/static/images/desktop.svg"></v-img>
          </div>
        </v-col>
        <v-col cols="12" sm="10" md="7">
          <v-card-title class="font-weight-black text-h5 text-sm-h4 pr-0">
            Découvrez les initiatives prises par nos cantines pour une alimentation saine, de qualité, et plus durable.
          </v-card-title>
        </v-col>
        <v-spacer></v-spacer>
      </v-row>
    </v-card>
    <v-row>
      <v-col v-for="canteen in publishedCanteens" :key="canteen.id" cols="12" md="6">
        <v-card :to="{ name: 'CanteenPage', params: { id: canteen.id } }" hover class="pa-4 text-left">
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
              <v-icon small class="mt-n1" color="secondary">mdi-check</v-icon>
              {{ initiative }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
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
  computed: {
    publishedCanteens() {
      return this.$store.state.publishedCanteens
    },
  },
}
</script>
