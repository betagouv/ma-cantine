<template>
  <v-card outlined class="fill-height d-flex flex-column dsfr">
    <v-card-title class="font-weight-bold body-1">
      <v-icon color="amber darken-2" class="mr-2">
        mdi-bullhorn
      </v-icon>
      <span>Information des convives</span>
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
  name: "InformationCard",
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
      return Constants.Levels.ADVANCED
    },
    cardBody() {
      return "Vous êtes au point ! N’hésitez pas à utiliser les outils fournis par “ma cantine” pour informer encore plus facilement vos convives de vos actions."
    },
  },
}
</script>
