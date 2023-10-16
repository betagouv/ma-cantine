<template>
  <v-card
    :to="diagnostic ? { name: 'DiagnosticModification', params: { canteenUrlComponent, year: diagnostic.year } } : null"
    outlined
    class="fill-height d-flex flex-column dsfr pa-6"
    style="background-color: #F6F6F6;"
  >
    <v-card-title class="mx-1">
      <v-icon small :color="keyMeasure.mdiIconColor" class="mr-2">
        {{ keyMeasure.mdiIcon }}
      </v-icon>
      <h3 class="fr-text font-weight-bold">
        {{ keyMeasure.shortTitle }}
      </h3>
    </v-card-title>
    <v-card-text v-if="needsData">
      <MissingDataChip class="mt-n4 ml-8" />
    </v-card-text>
    <v-card-text :class="`mt-n4 pl-12 ${level.colorClass}`" v-else>
      <p class="mb-0 mt-2 fr-text-xs">
        NIVEAU :
        <span class="font-weight-black">{{ level.text }}</span>
      </p>
    </v-card-text>
    <v-card-text class="fr-text-xs pb-0">
      <p class="mb-0">{{ cardBody }}</p>
    </v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions class="px-4">
      <v-spacer></v-spacer>
      <v-icon color="primary" class="mr-n1">$arrow-right-line</v-icon>
    </v-card-actions>
  </v-card>
</template>

<script>
import Constants from "@/constants"
import MissingDataChip from "./MissingDataChip"
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "DiversificationCard",
  components: { MissingDataChip },
  props: {
    diagnostic: {
      type: Object,
    },
    canteen: {
      type: Object,
      required: true,
    },
  },
  computed: {
    keyMeasure() {
      return keyMeasures.find((x) => x.id === "diversification-des-menus")
    },
    needsData() {
      return this.level === Constants.Levels.UNKNOWN
    },
    level() {
      return Constants.Levels.BEGINNER
    },
    cardBody() {
      return "Faites un premier pas : mettez en place un menu végétarien par semaine. Découvrez des recettes et des conseils directement sur « ma cantine » !"
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
  },
}
</script>
