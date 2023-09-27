<template>
  <v-card outlined class="fill-height">
    <v-card-title class="font-weight-bold body-1">
      <v-icon color="green darken-1" class="mr-2">
        $leaf-fill
      </v-icon>
      <span>Diversification des menus</span>
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
  name: "DiversificationCard",
  computed: {
    level() {
      return Constants.Levels.BEGINNER
    },
    cardBody() {
      return "Faites un premier pas : mettez en place un menu végétarien par semaine. Découvrez des recettes et des conseils directement sur “ma cantine” !"
    },
  },
}
</script>
