<template>
  <div class="pa-8 pb-4">
    <v-row v-if="diagnostic">
      <v-col cols="12" md="8">
        <h3 class="fr-h6 font-weight-bold mb-0">
          {{ keyMeasure.title }}
        </h3>
        <v-btn text color="primary" class="px-0" @click="() => (showIntro = !showIntro)">
          En savoir plus
        </v-btn>
      </v-col>
      <v-col class="fr-text-xs text-right">
        <p class="mb-0">Votre niveau : {{ level }}</p>
        <p class="grey--text text--darken-2 mb-0">
          {{ levelMessage }}
        </p>
      </v-col>
    </v-row>
    <h3 v-else class="fr-h6 font-weight-bold mb-4">
      {{ keyMeasure.title }}
    </h3>
    <div v-if="!diagnostic || showIntro">
      <component
        :is="`${keyMeasure.baseComponent}Info`"
        :diagnostic="diagnostic"
        :centralDiagnostic="centralDiagnostic"
      />
      <p><i>Sauf mention contraire, toutes les questions sont obligatoires.</i></p>
      <v-btn
        v-if="measureId !== establishmentId && !diagnostic && !usesOtherDiagnosticForMeasure(measureId)"
        color="primary"
        :to="{ name: 'NewDiagnosticForCanteen', params: { canteenUrlComponent }, query: { année: year } }"
        class="mt-4"
      >
        Commencer
      </v-btn>
    </div>
    <div v-if="diagnostic">
      <hr aria-hidden="true" role="presentation" class="mt-4 mb-8" />
      <v-row class="mb-4">
        <v-col class="d-flex align-end">
          <h4 class="fr-text-sm font-weight-bold">SYNTHÈSE</h4>
        </v-col>
        <v-col class="text-right">
          <v-btn
            v-if="!hasActiveTeledeclaration"
            outlined
            small
            color="primary"
            class="fr-btn--tertiary px-2"
            :to="{ name: 'DiagnosticModification', params: { canteenUrlComponent, year: diagnostic.year } }"
          >
            <v-icon small class="mr-2">$pencil-line</v-icon>
            Modifier mes données
          </v-btn>
        </v-col>
      </v-row>
      <component
        :is="`${keyMeasure.baseComponent}Info`"
        :diagnostic="diagnostic"
        :centralDiagnostic="centralDiagnostic"
      />
    </div>
    <v-row class="mt-6">
      <v-col cols="6">
        <router-link :to="{}">Previous tab</router-link>
      </v-col>
      <v-col cols="6" class="text-right">
        <router-link :to="{}">Next tab</router-link>
      </v-col>
    </v-row>
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
      showIntro: false,
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
    hasActiveTeledeclaration() {
      return false
    },
    level() {
      return "EXPERT"
    },
    levelMessage() {
      return "Vous êtes au point, bravo ! Partagez vos meilleures idées pour inspirer d'autres cantines !"
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

<style scoped>
hr {
  border: none;
  height: 1px;
  /* Set the hr color */
  color: #ddd; /* old IE */
  background-color: #ddd; /* Modern Browsers */
}
</style>
