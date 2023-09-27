<template>
  <v-card outlined class="fill-height">
    <v-card-title class="font-weight-bold body-1">
      <v-icon color="blue darken-1" class="mr-2">
        mdi-weather-windy
      </v-icon>
      <span>Interdiction du plastique</span>
    </v-card-title>
    <v-card-text :class="level.colorClass">
      NIVEAU :
      <span class="font-weight-bold">{{ level.text }}</span>
    </v-card-text>
    <v-card-text>{{ cardBody }}</v-card-text>
  </v-card>
</template>

<script>
import Constants from "@/constants"

export default {
  name: "NoPlasticCard",
  computed: {
    level() {
      return Constants.Levels.UNKNOWN
    },
    cardBody() {
      return "Bravo pour vos actions ! Continuez à substituer les matières plastiques : et si vous disiez au revoir aux ustensiles à usage unique ?"
    },
  },
}
</script>
