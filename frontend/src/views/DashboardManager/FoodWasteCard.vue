<template>
  <v-card
    :to="{ name: 'DiagnosticModification', params: { canteenUrlComponent, year: diagnostic.year } }"
    outlined
    class="fill-height d-flex flex-column dsfr"
  >
    <v-card-title class="font-weight-bold body-1">
      <v-icon color="orange darken-2" class="mr-2">
        mdi-offer
      </v-icon>
      <span>Lutte contre le gaspillage</span>
    </v-card-title>
    <v-card-text v-if="needsData">
      <MissingDataChip class="mt-n4 ml-8" />
    </v-card-text>
    <v-card-text :class="`mt-n4 pl-12 ${level.colorClass}`" v-else>
      NIVEAU :
      <span class="font-weight-bold">{{ level.text }}</span>
    </v-card-text>
    <v-card-text>{{ cardBody }}</v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions class="px-4 pt-0">
      <v-spacer></v-spacer>
      <v-icon color="primary">$arrow-right-line</v-icon>
    </v-card-actions>
  </v-card>
</template>

<script>
import Constants from "@/constants"
import MissingDataChip from "./MissingDataChip.vue"

export default {
  name: "FoodWasteCard",
  components: { MissingDataChip },
  props: {
    diagnostic: {
      type: Object,
    },
    canteen: {
      type: Object,
    },
  },
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
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
  },
}
</script>
