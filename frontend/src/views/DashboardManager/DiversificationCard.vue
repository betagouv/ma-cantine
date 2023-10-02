<template>
  <v-card
    :to="{ name: 'DiagnosticModification', params: { canteenUrlComponent, year: diagnostic.year } }"
    outlined
    class="fill-height d-flex flex-column dsfr"
  >
    <v-card-title class="font-weight-bold body-1">
      <v-icon color="green darken-1" class="mr-2">
        $leaf-fill
      </v-icon>
      <span>Diversification des menus</span>
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
  name: "DiversificationCard",
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
      return Constants.Levels.BEGINNER
    },
    cardBody() {
      return "Faites un premier pas : mettez en place un menu végétarien par semaine. Découvrez des recettes et des conseils directement sur “ma cantine” !"
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
  },
}
</script>
