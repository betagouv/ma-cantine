<template>
  <v-card
    class="d-flex"
    :to="{ name: 'DiagnosticModification', params: { canteenUrlComponent, year: diagnostic.year } }"
  >
    <v-sheet color="grey lighten-4" width="150" class="d-flex flex-column justify-center px-4">
      <div class="text-h3 grey--text font-weight-black text-center">{{ diagnostic.year }}</div>
    </v-sheet>
    <v-col cols="6">
      <v-card-title class="font-weight-bold">{{ canteen.name }}</v-card-title>
      <v-card-subtitle>{{ dataStatus }}</v-card-subtitle>
    </v-col>
    <v-spacer></v-spacer>
    <v-card-text class="align-self-center">Ouvert {{ timeAgo(diagnostic.creationDate, true) }}</v-card-text>
  </v-card>
</template>

<script>
import { timeAgo } from "@/utils"

export default {
  name: "DiagnosticCard",
  props: {
    diagnostic: {
      type: Object,
      required: true,
    },
  },
  computed: {
    canteen() {
      return this.$store.state.userCanteens.find((canteen) =>
        canteen.diagnostics.some((diagnostic) => diagnostic.id === this.diagnostic.id)
      )
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
    dataStatus() {
      let status = "Données d'appro incomplètes"
      if (this.canteen.isPublished) {
        status = "Données publiées"
      } else {
        const approComplete = ["valueBioHt", "valueSustainableHt", "valueTotalHt"].every(
          // sadly null >= 0 is true
          (key) => this.diagnostic[key] > 0 || this.diagnostic[key] === 0
        )
        status = approComplete ? "Données complètées" : status
      }
      return status
    },
  },
  methods: {
    timeAgo: timeAgo,
  },
}
</script>

<style scoped>
.v-sheet {
  border-radius: 0;
}
</style>
