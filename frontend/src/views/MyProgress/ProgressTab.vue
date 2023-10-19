<template>
  <div class="pa-8 pb-4">
    <h3 class="fr-text font-weight-bold mb-4">
      {{ keyMeasure.title }}
    </h3>
    <component
      :is="`${keyMeasure.baseComponent}Info`"
      :diagnostic="diagnostic"
      :centralDiagnostic="centralDiagnostic"
    />
    <p><i>Sauf mention contraire, toutes les questions sont obligatoires.</i></p>
    <div v-if="measureId !== establishmentId" class="pt-4">
      <v-btn
        v-if="diagnostic && !usesOtherDiagnosticForMeasure(measureId)"
        outlined
        color="primary"
        :to="{ name: 'DiagnosticModification', params: { canteenUrlComponent, year: diagnostic.year } }"
      >
        Modifier
      </v-btn>
      <v-btn
        v-else-if="!diagnostic && !usesOtherDiagnosticForMeasure(measureId)"
        color="primary"
        :to="{ name: 'NewDiagnosticForCanteen', params: { canteenUrlComponent }, query: { année: year } }"
      >
        Commencer
      </v-btn>
    </div>
  </div>
</template>

<script>
import QualityMeasureInfo from "./introduction/ApproProgress"
import DiversificationMeasureInfo from "./introduction/DiversificationProgress"
import InformationMeasureInfo from "./introduction/InfoProgress"
import NoPlasticMeasureInfo from "./introduction/PlasticProgress"
import WasteMeasureInfo from "./introduction/WasteProgress"
import CanteenProgressInfo from "./introduction/CanteenProgress"
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "ProgressTab",
  props: {
    measureId: {
      type: String,
      required: true,
    },
    year: {
      type: String,
      required: true,
    },
    canteen: {
      type: Object,
      required: true,
    },
    diagnostic: Object,
    centralDiagnostic: Object,
  },
  components: {
    QualityMeasureInfo,
    DiversificationMeasureInfo,
    InformationMeasureInfo,
    NoPlasticMeasureInfo,
    WasteMeasureInfo,
    CanteenProgressInfo,
  },
  data() {
    return {
      approId: "produits-de-qualite",
      establishmentId: "etablissement",
    }
  },
  computed: {
    keyMeasure() {
      if (this.measureId === this.establishmentId) {
        return { title: "Établissement", baseComponent: "CanteenProgress" }
      }
      return keyMeasures.find((x) => x.id === this.measureId)
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
  },
  methods: {
    usesOtherDiagnosticForMeasure(id) {
      const isApproTab = id === this.approId
      if (this.canteen?.productionType === "site") {
        return false
      } else if (this.canteen?.productionType === "site_cooked_elsewhere") {
        if (isApproTab) return !!this.centralDiagnostic
        if (this.centralDiagnostic?.centralKitchenDiagnosticMode === "ALL") {
          return !!this.centralDiagnostic
        }
      } else {
        // both CC production types
        if (!isApproTab) {
          const satelliteProvidesOtherMeasures = this.diagnostic?.centralKitchenDiagnosticMode === "APPRO"
          return satelliteProvidesOtherMeasures
        }
      }
      return false
    },
  },
}
</script>
