<template>
  <v-card outlined class="fill-height d-flex flex-column dsfr">
    <v-card-title class="font-weight-bold body-1">
      <v-icon color="blue darken-1" class="mr-2">
        mdi-weather-windy
      </v-icon>
      <span>Interdiction du plastique</span>
    </v-card-title>
    <v-card-text v-if="needsData">
      <MissingDataChip />
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
  name: "NoPlasticCard",
  components: { MissingDataChip },
  props: {
    diagnostic: {
      type: Object,
    },
  },
  computed: {
    needsData() {
      return this.level === Constants.Levels.UNKNOWN
    },
    level() {
      return Constants.Levels.UNKNOWN
    },
    cardBody() {
      return "Bravo pour vos actions ! Continuez à substituer les matières plastiques : et si vous disiez au revoir aux ustensiles à usage unique ?"
    },
  },
}
</script>
