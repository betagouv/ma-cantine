<template>
  <v-card :to="link" outlined class="fill-height d-flex flex-column dsfr">
    <v-card-title class="font-weight-bold body-1">
      <v-icon :color="keyMeasure.mdiIconColor" class="mr-2">
        {{ keyMeasure.mdiIcon }}
      </v-icon>
      <h3>{{ keyMeasure.shortTitle }}</h3>
    </v-card-title>
    <v-card-text v-if="needsData">
      <MissingDataChip class="mt-n4 ml-8" />
    </v-card-text>
    <v-card-text :class="`mt-n4 pl-12 ${level.colorClass}`" v-else>
      NIVEAU :
      <span class="font-weight-bold">{{ level.text }}</span>
    </v-card-text>
    <v-card-text>
      <p>{{ cardBody }}</p>
    </v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions class="px-4 pt-0">
      <v-spacer></v-spacer>
      <v-icon color="primary">$arrow-right-line</v-icon>
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
  data() {
    return {
      measureId: "diversification-des-menus",
    }
  },
  computed: {
    keyMeasure() {
      return keyMeasures.find((x) => x.id === this.measureId)
    },
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
    link() {
      return this.diagnostic
        ? {
            name: "MyProgress",
            params: {
              canteenUrlComponent: this.canteenUrlComponent,
              year: this.diagnostic.year,
              measure: this.measureId,
            },
          }
        : null
    },
  },
}
</script>
