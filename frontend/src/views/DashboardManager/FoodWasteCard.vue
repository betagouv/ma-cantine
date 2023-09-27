<template>
  <v-card outlined class="fill-height">
    <v-card-title class="font-weight-bold body-1">
      <v-icon color="orange darken-2" class="mr-2">
        mdi-offer
      </v-icon>
      <span>Lutte contre le gaspillage</span>
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
  name: "FoodWasteCard",
  computed: {
    level() {
      return Constants.Levels.EXPERT
    },
    cardBody() {
      return "Bravo pour vos actions ! Pour aller plus loin dans la lutte contre le gaspillage, et si vous rendiez la pré-inscription des convives obligatoires ?"
    },
  },
}
</script>
