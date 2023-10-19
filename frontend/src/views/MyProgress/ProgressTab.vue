<template>
  <div class="pa-8 pb-4">
    <h3 class="fr-text font-weight-bold mb-4">
      {{ keyMeasure.title }}
    </h3>
    <component :is="progressComponents[measureId]" :diagnostic="diagnostic" :centralDiagnostic="centralDiagnostic" />
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
    measureId: {
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
      approId: "produits-de-qualite",
      establishmentId: "etablissement",
      progressComponents: {
        "produits-de-qualite": ApproProgress,
        "gaspillage-alimentaire": WasteProgress,
        "diversification-des-menus": DiversificationProgress,
        "interdiction-du-plastique": PlasticProgress,
        "information-convives": InfoProgress,
        etablissement: CanteenProgress,
      },
    }
  },
  computed: {
    keyMeasure() {
      if (this.measureId === this.establishmentId) {
        return { title: "Établissement" }
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
