<template>
  <v-card :to="link" outlined class="fill-height d-flex flex-column dsfr pa-6" style="background-color: #F6F6F6;">
    <v-card-title class="mx-1">
      <v-icon small :color="keyMeasure.mdiIconColor" class="mr-2">
        {{ keyMeasure.mdiIcon }}
      </v-icon>
      <h3 class="fr-text font-weight-bold">{{ keyMeasure.shortTitle }}</h3>
    </v-card-title>
    <v-card-text v-if="!delegatedToCentralKitchen && needsData">
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
  name: "InformationCard",
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
      measureId: "information-des-usagers",
    }
  },
  computed: {
    keyMeasure() {
      return keyMeasures.find((x) => x.id === this.measureId)
    },
    needsData() {
      const hasActiveTeledeclaration = this.diagnostic?.isTeledeclared
      return !hasActiveTeledeclaration && !this.delegatedToCentralKitchen && this.level === Constants.Levels.UNKNOWN
    },
    level() {
      if (this.delegatedToSatellite) return null
      if (!hasStartedMeasureTunnel(this.diagnostic, this.keyMeasure)) return Constants.Levels.UNKNOWN
      return null
    },
    cardBody() {
      if (this.delegatedToSatellite) {
        return "Les données associées à cette mesure EGalim sont renseignées au niveau des restaurants satellites de votre groupe."
      } else if (this.delegatedToCentralKitchen) {
        return "Votre cuisine centrale a renseigné les données de cette mesure à votre place."
      }
      return "Tous les ans, informer les convives et leurs proches de la qualité alimentaire et nutritionnelle des repas servis."
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
