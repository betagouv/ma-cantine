<template>
  <div class="pa-8 pb-4">
    <h3 class="fr-text font-weight-bold mb-4">
      {{ keyMeasure.title }}
    </h3>
    <component :is="progressComponents[measureIndex]" :diagnostic="diagnostic" :centralDiagnostic="centralDiagnostic" />
    <p><i>Sauf mention contraire, toutes les questions sont obligatoires.</i></p>
    <div v-if="measureIndex < 5" class="pt-4">
      <v-btn
        v-if="diagnostic && !usesOtherDiagnosticForMeasure(measureIndex)"
        outlined
        color="primary"
        :to="{ name: 'DiagnosticModification', params: { canteenUrlComponent, year: diagnostic.year } }"
      >
        Modifier
      </v-btn>
      <v-btn
        v-else-if="!diagnostic && !usesOtherDiagnosticForMeasure(measureIndex)"
        color="primary"
        :to="{ name: 'NewDiagnosticForCanteen', params: { canteenUrlComponent }, query: { année: year } }"
      >
        Commencer
      </v-btn>
    </div>
  </div>
</template>

<script>
import ApproProgress from "./ApproProgress"
import DiversificationProgress from "./DiversificationProgress"
import InfoProgress from "./InfoProgress"
import PlasticProgress from "./PlasticProgress"
import WasteProgress from "./WasteProgress"
import CanteenProgress from "./CanteenProgress"
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "ProgressTab",
  props: {
    measureIndex: {
      type: Number,
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
    ApproProgress,
    DiversificationProgress,
    InfoProgress,
    PlasticProgress,
    WasteProgress,
    CanteenProgress,
  },
  data() {
    return {
      progressComponents: [
        ApproProgress,
        WasteProgress,
        DiversificationProgress,
        PlasticProgress,
        InfoProgress,
        CanteenProgress,
      ],
    }
  },
  computed: {
    keyMeasure() {
      return keyMeasures.find((x) => x.id === "gaspillage-alimentaire")
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
  },
  methods: {
    usesOtherDiagnosticForMeasure(index) {
      const isApproTab = index === 0
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

<style></style>
