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
      <h3 class="fr-text font-weight-bold">{{ keyMeasure.shortTitle }}</h3>
    </v-card-title>
    <v-card-text v-if="needsData">
      <DataInfoChip :missingData="needsData" class="mt-n4 ml-8" />
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
import DataInfoChip from "./DataInfoChip"
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "NoPlasticCard",
  components: { DataInfoChip },
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
      return keyMeasures.find((x) => x.id === "interdiction-du-plastique")
    },
    needsData() {
      return this.level === Constants.Levels.UNKNOWN
    },
    level() {
      return Constants.Levels.UNKNOWN
    },
    cardBody() {
      return "Bravo pour vos actions ! Continuez à substituer les matières plastiques : et si vous disiez au revoir aux ustensiles à usage unique ?"
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
  },
}
</script>
