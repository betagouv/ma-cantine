<template>
  <div class="fr-text" v-if="hasApproData">
    <ApproGraph :diagnostic="diagnostic" :canteen="canteen" />
    <v-row>
      <v-col cols="12" md="6">
        <p>Détail du calcul de mes taux EGAlim</p>
        TODO
      </v-col>
      <v-col cols="12" md="6">
        <p>Par famille de produits</p>
        TODO
      </v-col>
    </v-row>
    <hr />
    <div>
      <p>Données détaillées</p>
      TODO only if simplified TODO button modifier
    </div>
  </div>
  <div class="fr-text" v-else>
    TODO
  </div>
</template>

<script>
import ApproGraph from "@/components/ApproGraph"
import { hasDiagnosticApproData } from "@/utils"

export default {
  name: "QualityMeasureSummary",
  components: { ApproGraph },
  props: {
    diagnostic: {},
    centralDiagnostic: {},
    canteen: {
      type: Object,
      required: true,
    },
  },
  computed: {
    usesCentralDiagnostic() {
      return this.centralDiagnostic?.centralKitchenDiagnosticMode === "ALL"
    },
    displayDiagnostic() {
      return this.usesCentralDiagnostic ? this.centralDiagnostic : this.diagnostic
    },
    hasApproData() {
      return hasDiagnosticApproData(this.displayDiagnostic)
    },
  },
}
</script>
