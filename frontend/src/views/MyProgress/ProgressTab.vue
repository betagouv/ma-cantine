<template>
  <div class="pa-8 pb-4">
    <div v-if="measureId !== establishmentId">
      <v-row v-if="diagnostic || hasCentralDiagnosticForMeasure">
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
      <div v-if="(!diagnostic && !hasCentralDiagnosticForMeasure) || showIntro">
        <component
          :is="`${keyMeasure.baseComponent}Info`"
          :canteen="canteen"
          :diagnostic="diagnostic"
          :centralDiagnostic="centralDiagnostic"
        />
        <p><i>Sauf mention contraire, toutes les questions sont obligatoires.</i></p>
        <v-btn
          v-if="measureId !== establishmentId && !diagnostic && !usesOtherDiagnosticForMeasure"
          color="primary"
          :to="{ name: 'NewDiagnosticForCanteen', params: { canteenUrlComponent }, query: { année: year } }"
          class="mt-4"
        >
          Commencer
        </v-btn>
      </div>
      <div v-if="diagnostic || hasCentralDiagnosticForMeasure" class="summary">
        <hr aria-hidden="true" role="presentation" class="mt-4 mb-8" />
        <div v-if="usesOtherDiagnosticForMeasure && isSatellite" class="fr-text pa-6 grey lighten-4 mb-6">
          <p class="mb-1 grey--text text--darken-4">
            Votre cantine sert des repas préparés par
            <span class="font-weight-bold">{{ centralKitchenName }}</span>
          </p>
          <p class="mb-0 grey--text text--darken-2">
            Votre cuisine centrale a déjà renseigné les données de cette mesure pour votre cantine. Retrouvez la
            synthèse ci-dessous.
            <span v-if="centralDiagnostic.centralKitchenDiagnosticMode !== 'ALL' && measureId === approId">
              Les autres volets de la loi EGAlim vous restent accessibles.
            </span>
          </p>
        </div>
        <v-row class="mb-4">
          <v-col class="d-flex align-end">
            <h4 class="fr-text-sm font-weight-bold my-1">SYNTHÈSE</h4>
          </v-col>
          <v-col class="text-right">
            <v-btn
              v-if="!hasActiveTeledeclaration && !usesOtherDiagnosticForMeasure"
              outlined
              small
              color="primary"
              class="fr-btn--tertiary px-2"
              :to="{ name: 'DiagnosticModification', params: { canteenUrlComponent, year: year } }"
            >
              <v-icon small class="mr-2">$pencil-line</v-icon>
              Modifier mes données
            </v-btn>
          </v-col>
        </v-row>
        <component
          :is="`${keyMeasure.baseComponent}Summary`"
          :canteen="canteen"
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
    <div v-else>
      <h3 class="fr-h6 font-weight-bold mb-4">
        Établissement
      </h3>
      <CanteenSummary :canteen="canteen" />
    </div>
  </div>
</template>

<script>
import QualityMeasureInfo from "./information/QualityMeasureInfo"
import DiversificationMeasureInfo from "./information/DiversificationMeasureInfo"
import InformationMeasureInfo from "./information/InformationMeasureInfo"
import NoPlasticMeasureInfo from "./information/NoPlasticMeasureInfo"
import WasteMeasureInfo from "./information/WasteMeasureInfo"
import QualityMeasureSummary from "./summary/QualityMeasureSummary"
import DiversificationMeasureSummary from "./summary/DiversificationMeasureSummary"
import InformationMeasureSummary from "./summary/InformationMeasureSummary"
import NoPlasticMeasureSummary from "./summary/NoPlasticMeasureSummary"
import WasteMeasureSummary from "./summary/WasteMeasureSummary"
import CanteenSummary from "./summary/CanteenSummary"
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "ProgressTab",
  props: {
    measureId: {
      type: String,
      required: true,
    },
    year: {
      type: Number,
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
    QualityMeasureSummary,
    DiversificationMeasureSummary,
    InformationMeasureSummary,
    NoPlasticMeasureSummary,
    WasteMeasureSummary,
    CanteenSummary,
  },
  data() {
    return {
      approId: "qualite-des-produits",
      establishmentId: "etablissement",
      showIntro: false,
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
    isSatellite() {
      return this.canteen.productionType === "site_cooked_elsewhere"
    },
    centralKitchenName() {
      if (!this.isSatellite) return null
      if (this.canteen.centralKitchen?.name) {
        return this.canteen.centralKitchen.name
      }
      return this.canteen.centralProducerSiret
        ? `l'établissement avec le SIRET ${this.canteen.centralProducerSiret}`
        : "un établissement inconnu"
    },
    usesOtherDiagnosticForMeasure() {
      const isApproTab = this.measureId === this.approId
      if (this.canteen.productionType === "site") {
        return false
      } else if (this.isSatellite) {
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
    hasActiveTeledeclaration() {
      return this.diagnostic?.teledeclaration?.status === "SUBMITTED"
    },
    level() {
      return "EXPERT"
    },
    levelMessage() {
      return "Vous êtes au point, bravo ! Partagez vos meilleures idées pour inspirer d'autres cantines !"
    },
    hasCentralDiagnosticForMeasure() {
      if (!this.centralDiagnostic) return false
      if (this.measureId === this.establishmentId) return false
      if (this.measureId === this.approId) return true
      return this.centralDiagnostic.centralKitchenDiagnosticMode === "ALL"
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
.summary >>> ul {
  list-style-type: none;
  padding-left: 0;
}
.summary >>> li {
  margin-bottom: 14px;
  display: flex;
}
.summary >>> li .v-icon {
  align-items: baseline;
}
</style>
