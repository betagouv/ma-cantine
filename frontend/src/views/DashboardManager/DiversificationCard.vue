<template>
  <v-card outlined class="fill-height">
    <v-card-title class="font-weight-bold body-1">
      <v-icon color="green darken-1" class="mr-2">
        $leaf-fill
      </v-icon>
      <span>Diversification des menus</span>
    </v-card-title>
    <v-card-text v-if="needsData">
      <MissingDataChip v-if="!hasPurchases && !hasCurrentDiagnostic && !hasLastYearDiagnostic" />
    </v-card-text>
    <v-card-text :class="level.colorClass" v-else>
      NIVEAU :
      <span class="font-weight-bold">{{ level.text }}</span>
    </v-card-text>
    <v-card-text>{{ cardBody }}</v-card-text>
  </v-card>
</template>

<script>
import Constants from "@/constants"
import MissingDataChip from "./MissingDataChip.vue"

export default {
  name: "DiversificationCard",
  components: { MissingDataChip },
  computed: {
    needsData() {
      return this.level === Constants.Levels.UNKNOWN
    },
    level() {
      return Constants.Levels.BEGINNER
    },
    cardBody() {
      return "Faites un premier pas : mettez en place un menu végétarien par semaine. Découvrez des recettes et des conseils directement sur “ma cantine” !"
    },
  },
}
</script>
