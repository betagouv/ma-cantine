<template>
  <v-card
    :class="{ 'd-flex': true, 'flex-column': $vuetify.breakpoint.smAndDown }"
    :to="{ name: 'DiagnosticModification', params: { canteenUrlComponent, year: diagnostic.year } }"
  >
    <v-sheet
      color="grey lighten-4"
      :width="$vuetify.breakpoint.smAndDown ? 'auto' : 150"
      class="d-flex flex-column justify-center px-4"
    >
      <div class="text-h3 grey--text font-weight-black text-center">{{ diagnostic.year }}</div>
    </v-sheet>
    <v-col cols="12" md="6" class="py-0">
      <v-card-title class="font-weight-bold">{{ canteen.name }}</v-card-title>
      <v-card-subtitle>{{ dataStatus }}</v-card-subtitle>
    </v-col>
    <v-spacer></v-spacer>
    <v-col cols="12" md="4" class="py-0">
      <v-card-text class="align-self-center">{{ dateText }}</v-card-text>
    </v-col>
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
    dateText() {
      console.log(timeAgo)
      const baseText = `Créé ${timeAgo(this.diagnostic.creationDate, true)}`
      const dateDifference = new Date(this.diagnostic.modificationDate) - new Date(this.diagnostic.creationDate)
      const showModificationDate = dateDifference > 1000 * 60 // one minute difference
      if (showModificationDate) return `${baseText}, modifié ${timeAgo(this.diagnostic.modificationDate, true)}`
      return baseText
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
