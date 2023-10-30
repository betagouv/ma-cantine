<template>
  <div class="fr-text" v-if="hasApproData">
    <ApproGraph :diagnostic="diagnostic" :canteen="canteen" />
    <v-row>
      <v-col cols="12" md="6">
        <p class="font-weight-bold">Détail du calcul de mes taux EGAlim</p>
        <v-row>
          <v-col cols="6">
            <p class="mb-0">Produits bio</p>
          </v-col>
          <v-col cols="2">
            <p class="mb-0 font-weight-bold">{{ bioPercentage }} %</p>
          </v-col>
          <v-col cols="4">
            <p class="mb-0">
              <i>objectif : {{ applicableRules.bioThreshold }} %</i>
            </p>
          </v-col>
        </v-row>
        <v-row class="mt-0">
          <v-col cols="6">
            <p class="mb-0">Produits durables et de qualité (hors bio)</p>
          </v-col>
          <v-col cols="2">
            <p class="mb-0 font-weight-bold">{{ sustainablePercentage }} %</p>
          </v-col>
        </v-row>
        <hr aria-hidden="true" role="presentation" class="my-6" />
        <v-row class="mt-0">
          <v-col cols="6">
            <p class="mb-0">Produits EGAlim</p>
          </v-col>
          <v-col cols="2">
            <p class="mb-0 font-weight-bold">{{ egalimPercentage }} %</p>
          </v-col>
          <v-col cols="4">
            <p class="mb-0">
              <i>objectif : {{ applicableRules.qualityThreshold }} %</i>
            </p>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="12" md="6">
        <p class="font-weight-bold">Par famille de produits</p>
        TODO
      </v-col>
    </v-row>
    <hr aria-hidden="true" role="presentation" class="mt-10 mb-4 faint" />
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
import { hasDiagnosticApproData, applicableDiagnosticRules, getSustainableTotal, getPercentage } from "@/utils"

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
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
    bioPercentage() {
      return (
        Math.round(this.diagnostic.percentageValueBioHt * 100) ||
        getPercentage(this.diagnostic.valueBioHt, this.diagnostic.valueTotalHt, true)
      )
    },
    sustainablePercentage() {
      return (
        Math.round(this.diagnostic.percentageValueSustainableHt * 100) ||
        getPercentage(getSustainableTotal(this.diagnostic), this.diagnostic.valueTotalHt, true)
      )
    },
    egalimPercentage() {
      return this.bioPercentage + this.sustainablePercentage
    },
  },
}
</script>

<style scoped>
hr.faint {
  border: none;
  height: 1px;
  /* Set the hr color */
  color: #ddd; /* old IE */
  background-color: #ddd; /* Modern Browsers */
}
</style>
