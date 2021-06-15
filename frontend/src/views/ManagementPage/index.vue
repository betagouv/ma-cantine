<template>
  <div class="text-left">
    <h1 class="text-center">Gérér mes cantines</h1>
    <div>
      <h2 class="my-4">Mes cantines</h2>
      <v-row>
        <v-col cols="4">
          <v-card v-for="canteen in canteens" :key="canteen.name">
            <v-card-title>{{ canteen.name }}</v-card-title>
            <v-card-subtitle v-if="canteen.dailyMealCount || canteen.city">
              <div v-if="canteen.siret">SIRET : {{ canteen.siret }}</div>
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
                {{ sectorsForCanteen(canteen) }}
              </div>
            </v-card-subtitle>
          </v-card>
        </v-col>
        <v-col cols="4" height="100%">
          <v-card class="fill-height">
            <v-icon xLarge>mdi-plus</v-icon>
            <v-spacer></v-spacer>
            <v-card-actions>
              <v-btn text>Ajouter une cantine</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </div>
    <div class="mt-8">
      <h2 class="my-4">Mes diagnostics</h2>
      <v-card v-for="diagnostic in diagnostics" :key="diagnostic.name" class="my-4">
        <v-card-title>{{ canteenForDiagnostic(diagnostic).name }}</v-card-title>
        <v-card-text>
          <v-row class="mx-1">
            <p>{{ diagnostic.year }}</p>
            <v-spacer></v-spacer>
            <p>{{ dataStatus(diagnostic) }}</p>
            <v-spacer></v-spacer>
            <p>Ouvert il y a {{ diagnostic.lastOpened }}</p>
            <v-spacer></v-spacer>
            <p>
              <v-icon>mdi-account-group</v-icon>
              {{ canteenForDiagnostic(diagnostic).managers.length }} gestionnaires
            </p>
          </v-row>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      canteens: [
        {
          name: "Test kitchen",
          dailyMealCount: 900,
          city: "Paris",
          siret: "987 654 321",
          sectors: ["Scolaire", "Administration"],
          managers: [0, 5, 8],
        },
      ],
      diagnostics: [
        {
          canteenId: 0,
          year: 2020,
          status: "PUBLISHED",
          lastOpened: "4 heures",
        },
        {
          canteenId: 0,
          year: 2021,
          status: "INCOMPLETE",
          lastOpened: "4 heures",
        },
      ],
    }
  },
  methods: {
    // TODO: consider how to share sector displays between views,
    // or perhaps refactor the subtitles to own component to share
    sectorsForCanteen(canteen) {
      return canteen.sectors.map((sector) => sector.toLowerCase()).join(", ")
    },
    dataStatus(diagnostic) {
      return {
        PUBLISHED: "Données complètées, sauvegardées, et publiées",
        INCOMPLETE: "Données incomplètées",
      }[diagnostic.status]
    },
    canteenForDiagnostic(diagnostic) {
      return this.canteens[diagnostic.canteenId]
    },
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
  },
}
</script>
