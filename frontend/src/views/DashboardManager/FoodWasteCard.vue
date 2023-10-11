<template>
  <v-card :to="link" outlined class="fill-height d-flex flex-column dsfr">
    <v-card-title class="font-weight-bold body-1">
      <v-icon :color="keyMeasure.mdiIconColor" class="mr-2">
        {{ keyMeasure.mdiIcon }}
      </v-icon>
      <h3>{{ keyMeasure.shortTitle }}</h3>
    </v-card-title>
    <v-card-text v-if="needsData">
      <MissingDataChip class="py-0 ml-8" />
    </v-card-text>
    <v-card-text :class="`py-0 pl-12 ${level.colorClass}`" v-else-if="!delegatedToSatellite">
      NIVEAU :
      <span class="font-weight-bold">{{ level.text }}</span>
    </v-card-text>
    <v-spacer />
    <v-card-text>
      <p>{{ cardBody }}</p>
    </v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions v-if="!delegatedToSatellite" class="px-4 pt-0">
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
  name: "FoodWasteCard",
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
      measureId: "gaspillage-alimentaire",
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
      return Constants.Levels.EXPERT
    },
    cardBody() {
      if (this.delegatedToSatellite) {
        return "Les données associées à cette mesure EGAlim sont renseignées au niveau de chaque lieu de service que vous livrez."
      }
      return "Bravo pour vos actions ! Pour aller plus loin dans la lutte contre le gaspillage, et si vous rendiez la pré-inscription des convives obligatoires ?"
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
    link() {
      return !this.delegatedToSatellite && this.diagnostic
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
    delegatedToSatellite() {
      return this.diagnostic?.centralKitchenDiagnosticMode === "APPRO"
    },
  },
}
</script>
