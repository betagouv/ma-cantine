<template>
  <v-card outlined class="fill-height">
    <v-card-title class="font-weight-bold body-1">
      <v-icon color="orange darken-2" class="mr-2">
        mdi-offer
      </v-icon>
      <span>Lutte contre le gaspillage</span>
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
  name: "FoodWasteCard",
  components: { MissingDataChip },
  computed: {
    needsData() {
      return this.level === Constants.Levels.UNKNOWN
    },
    level() {
      return Constants.Levels.EXPERT
    },
    cardBody() {
      return "Bravo pour vos actions ! Pour aller plus loin dans la lutte contre le gaspillage, et si vous rendiez la pré-inscription des convives obligatoires ?"
    },
  },
}
</script>
