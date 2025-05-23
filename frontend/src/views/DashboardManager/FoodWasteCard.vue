<template>
  <v-card :to="link" outlined class="fill-height d-flex flex-column dsfr pa-6" style="background-color: #F6F6F6;">
    <v-card-title class="mx-1">
      <v-icon small :color="keyMeasure.mdiIconColor" class="mr-2">
        {{ keyMeasure.mdiIcon }}
      </v-icon>
      <h3 class="fr-text font-weight-bold">{{ keyMeasure.shortTitle }}</h3>
    </v-card-title>
    <v-card-text v-if="!delegatedToCentralKitchen">
      <KeyMeasureBadge class="py-0 ml-8" :canteen="canteen" :diagnostic="diagnostic" :year="year" :id="measureId" />
    </v-card-text>
    <v-card-text v-if="!needsData && level" :class="`mt-n4 pl-12 ${level.colorClass}`">
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
import KeyMeasureBadge from "@/components/KeyMeasureBadge"
import keyMeasures from "@/data/key-measures.json"
import { hasStartedMeasureTunnel, delegatedToCentralKitchen } from "@/utils"

export default {
  name: "FoodWasteCard",
  components: { KeyMeasureBadge },
  props: {
    diagnostic: {
      type: Object,
    },
    canteen: {
      type: Object,
      required: true,
    },
    year: Number,
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
      const hasActiveTeledeclaration = this.diagnostic?.teledeclaration?.status === "SUBMITTED"
      return !hasActiveTeledeclaration && !this.delegatedToCentralKitchen && this.level === Constants.Levels.UNKNOWN
    },
    level() {
      if (this.delegatedToSatellite) return null
      if (!hasStartedMeasureTunnel(this.diagnostic, this.keyMeasure)) return Constants.Levels.UNKNOWN
      return null
    },
    cardBody() {
      if (this.delegatedToSatellite) {
        return "Les données associées à cette mesure EGalim sont renseignées au niveau de chaque lieu de service que vous livrez."
      } else if (this.delegatedToCentralKitchen) {
        return "Votre livreur a renseigné les données de cette mesure à votre place."
      }
      return "Analyser votre situation, mettre en place des solutions comme la réservation de repas, et valoriser les restes par des dons aux associations."
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
      return delegatedToCentralKitchen(this.canteen, this.diagnostic)
    },
  },
}
</script>
