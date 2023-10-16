<template>
  <v-card :to="link" outlined class="fill-height d-flex flex-column dsfr pa-6" style="background-color: #F6F6F6;">
    <v-card-title class="mx-1">
      <v-icon small :color="keyMeasure.mdiIconColor" class="mr-2">
        {{ keyMeasure.mdiIcon }}
      </v-icon>
      <h3 class="fr-text font-weight-bold">{{ keyMeasure.shortTitle }}</h3>
    </v-card-title>
    <v-card-text v-if="needsData">
      <MissingDataChip class="py-0 ml-8" />
    </v-card-text>
    <v-card-text :class="`mt-n4 pl-12 ${level.colorClass}`" v-else-if="!delegatedToSatellite">
      <p class="mb-0 mt-2 fr-text-xs">
        NIVEAU :
        <span class="font-weight-black">{{ level.text }}</span>
      </p>
    </v-card-text>
    <v-card-text class="fr-text-xs pb-0">
      <p class="mb-0">{{ cardBody }}</p>
    </v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions v-if="!delegatedToSatellite" class="px-4">
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
  name: "InformationCard",
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
      measureId: "information-des-usagers",
    }
  },
  computed: {
    keyMeasure() {
      return keyMeasures.find((x) => x.id === this.measureId)
    },
    needsData() {
      const isSatellite = this.canteen.productionType === "site_cooked_elsewhere"
      const usesCentralDiag = isSatellite && this.diagnostic?.canteenId !== this.canteen.id
      const delegatedToCentralKitchen = usesCentralDiag && this.diagnostic?.centralKitchenDiagnosticMode === "ALL"
      return !delegatedToCentralKitchen && this.level === Constants.Levels.UNKNOWN
    },
    level() {
      return Constants.Levels.ADVANCED
    },
    cardBody() {
      if (this.delegatedToSatellite) {
        return "Les données associées à cette mesure EGAlim sont renseignées au niveau de chaque lieu de service que vous livrez."
      }
      return "Vous êtes au point ! N’hésitez pas à utiliser les outils fournis par « ma cantine » pour informer encore plus facilement vos convives de vos actions."
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
