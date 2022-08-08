<template>
  <v-card
    outlined
    :ripple="false"
    :class="{ 'd-flex': true, 'flex-column': $vuetify.breakpoint.xsOnly, dsfr: true }"
    :to="{ name: 'DiagnosticModification', params: { canteenUrlComponent, year: diagnostic.year } }"
  >
    <v-sheet
      color="grey lighten-4"
      :width="$vuetify.breakpoint.xsOnly ? 'auto' : 150"
      class="d-flex flex-column justify-center px-4"
    >
      <div class="text-h3 grey--text text--darken-1 font-weight-black text-center">{{ diagnostic.year }}</div>
    </v-sheet>
    <v-row>
      <v-col cols="7">
        <v-card-title class="font-weight-bold">{{ canteen.name || `SIRET : ${canteen.siret}` }}</v-card-title>
        <v-card-subtitle class="caption">
          <v-icon v-if="hasActiveTeledeclaration" color="green" small class="mt-0">mdi-check-circle</v-icon>
          {{ dataStatus }}
        </v-card-subtitle>
      </v-col>
      <v-spacer v-if="$vuetify.breakpoint.smAndUp"></v-spacer>
      <v-col cols="5" class="align-self-center">
        <v-card-text>{{ dateText }}</v-card-text>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import { timeAgo, isDiagnosticComplete } from "@/utils"

export default {
  name: "DiagnosticCard",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
    diagnostic: {
      type: Object,
      required: true,
    },
  },
  computed: {
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
    dataStatus() {
      let status = "Données manquantes"
      if (this.hasActiveTeledeclaration) {
        status = "Données télédéclarées"
      } else {
        const approComplete = isDiagnosticComplete(this.diagnostic)
        status = approComplete ? "Données d'approvisionnement complétées" : status
      }
      return status
    },
    dateText() {
      const baseText = `Créé ${timeAgo(this.diagnostic.creationDate, true)}`
      const dateDifference = new Date(this.diagnostic.modificationDate) - new Date(this.diagnostic.creationDate)
      const showModificationDate = dateDifference > 1000 * 60 // one minute difference
      if (showModificationDate) return `${baseText}, modifié ${timeAgo(this.diagnostic.modificationDate, true)}`
      return baseText
    },
    hasActiveTeledeclaration() {
      return this.diagnostic.teledeclaration && this.diagnostic.teledeclaration.status === "SUBMITTED"
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
