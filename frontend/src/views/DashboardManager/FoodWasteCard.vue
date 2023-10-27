<template>
  <v-card :to="link" outlined class="fill-height d-flex flex-column dsfr pa-6" style="background-color: #F6F6F6;">
    <v-card-title class="mx-1">
      <v-icon small :color="keyMeasure.mdiIconColor" class="mr-2">
        {{ keyMeasure.mdiIcon }}
      </v-icon>
      <h3 class="fr-text font-weight-bold">{{ keyMeasure.shortTitle }}</h3>
    </v-card-title>
    <v-card-text v-if="needsData">
      <DataInfoBadge :missingData="needsData" class="py-0 ml-8" />
    </v-card-text>
    <v-card-text :class="`mt-n4 pl-12 ${level.colorClass}`" v-else-if="!delegatedToSatellite">
      <p class="mb-0 mt-2 fr-text-xs">
        NIVEAU :
        <span class="font-weight-black">{{ level.text }}</span>
      </p>
    </v-card-text>
    <v-card-text class="fr-text-xs">
      <p class="mb-0">{{ cardBody }}</p>
    </v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions v-if="!delegatedToSatellite" class="px-4 pt-0 mt-n2">
      <v-spacer></v-spacer>
      <v-icon color="primary" class="mr-n1">$arrow-right-line</v-icon>
    </v-card-actions>
  </v-card>
</template>

<script>
import Constants from "@/constants"
import DataInfoBadge from "./DataInfoBadge"
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "FoodWasteCard",
  components: { DataInfoBadge },
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
      return !this.delegatedToCentralKitchen && this.level === Constants.Levels.UNKNOWN
    },
    level() {
      return Constants.Levels.EXPERT
    },
    cardBody() {
      if (this.delegatedToSatellite) {
        return "Les données associées à cette mesure EGAlim sont renseignées au niveau de chaque lieu de service que vous livrez."
      } else if (this.delegatedToCentralKitchen) {
        return "Votre cuisine centrale a renseigné les données de cette mesure à votre place."
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
    delegatedToCentralKitchen() {
      const isSatellite = this.canteen.productionType === "site_cooked_elsewhere"
      const usesCentralDiag = isSatellite && this.diagnostic?.canteenId === this.canteen.centralKitchen?.id
      return usesCentralDiag && this.diagnostic?.centralKitchenDiagnosticMode === "ALL"
    },
  },
}
</script>
