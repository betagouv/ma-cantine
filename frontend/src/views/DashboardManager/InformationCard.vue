<template>
  <v-card outlined class="fill-height">
    <v-card-title class="font-weight-bold body-1">
      <v-icon color="amber darken-2" class="mr-2">
        mdi-bullhorn
      </v-icon>
      <span>Information des convives</span>
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
  name: "InformationCard",
  computed: {
    level() {
      return Constants.Levels.ADVANCED
    },
    cardBody() {
      return "Vous êtes au point ! N’hésitez pas à utiliser les outils fournis par “ma cantine” pour informer encore plus facilement vos convives de vos actions."
    },
  },
}
</script>
