<template>
  <div class="pa-8 pb-4">
    <div>
      <v-row v-if="!showIntroduction && !isCanteenTab">
        <v-col cols="12" md="8">
          <h3 class="fr-h6 font-weight-bold mb-0">
            {{ keyMeasure.title }}
          </h3>
          <v-btn text color="primary" class="px-0" @click="() => (expandIntro = !expandIntro)">
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
      <div v-if="showIntroduction || expandIntro">
        <component :is="`${keyMeasure.baseComponent}Info`" :canteen="canteen" />
        <p><i>Sauf mention contraire, toutes les questions sont obligatoires.</i></p>
        <v-btn v-if="showIntroduction" color="primary" :disabled="requestOngoing" @click="startTunnel" class="mt-4">
          Commencer
        </v-btn>
      </div>
      <div v-if="showPurchasesSection">
        <hr aria-hidden="true" role="presentation" class="mt-4 mb-8" />
        <PurchasesSummary :canteen="canteen" />
      </div>
      <div v-else-if="showSynthesis">
        <hr aria-hidden="true" role="presentation" class="mt-4 mb-8" />
        <div
          v-if="!isCanteenTab && usesOtherDiagnosticForMeasure && isSatellite"
          class="fr-text pa-6 grey lighten-4 mb-6"
        >
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
              v-if="isCanteenTab || (!hasActiveTeledeclaration && !usesOtherDiagnosticForMeasure)"
              outlined
              small
              color="primary"
              class="fr-btn--tertiary px-2"
              :to="modificationLink"
            >
              <v-icon small class="mr-2">$pencil-line</v-icon>
              Modifier mes données
            </v-btn>
            <v-btn
              v-else-if="hasActiveTeledeclaration"
              outlined
              small
              color="primary"
              class="fr-btn--tertiary px-2"
              :disabled="true"
            >
              <v-icon small class="mr-2">$check-line</v-icon>
              Données télédéclarées
            </v-btn>
          </v-col>
        </v-row>
        <component
          :is="`${keyMeasure.baseComponent}Summary`"
          :usesCentralDiagnostic="hasCentralDiagnosticForMeasure"
          :canteen="canteen"
          :diagnostic="displayDiagnostic"
        />
      </div>
    </div>
  </div>
</template>

<script>
import QualityMeasureInfo from "./information/QualityMeasureInfo"
import DiversificationMeasureInfo from "./information/DiversificationMeasureInfo"
import InformationMeasureInfo from "./information/InformationMeasureInfo"
import NoPlasticMeasureInfo from "./information/NoPlasticMeasureInfo"
import WasteMeasureInfo from "./information/WasteMeasureInfo"
import QualityMeasureSummary from "@/components/DiagnosticSummary/QualityMeasureSummary"
import DiversificationMeasureSummary from "@/components/DiagnosticSummary/DiversificationMeasureSummary"
import InformationMeasureSummary from "@/components/DiagnosticSummary/InformationMeasureSummary"
import NoPlasticMeasureSummary from "@/components/DiagnosticSummary/NoPlasticMeasureSummary"
import WasteMeasureSummary from "@/components/DiagnosticSummary/WasteMeasureSummary"
import CanteenSummary from "@/components/DiagnosticSummary/CanteenSummary"
import PurchasesSummary from "@/components/DiagnosticSummary/PurchasesSummary"
import keyMeasures from "@/data/key-measures.json"
import { hasDiagnosticApproData, lastYear, hasStartedMeasureTunnel } from "@/utils"

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
    PurchasesSummary,
  },
  data() {
    return {
      approId: "qualite-des-produits",
      establishmentId: "etablissement",
      expandIntro: false,
      requestOngoing: false,
    }
  },
  computed: {
    isApproTab() {
      return this.measureId === this.approId
    },
    isCanteenTab() {
      return this.measureId === this.establishmentId
    },
    keyMeasure() {
      if (this.isCanteenTab) {
        return { title: "Données relatives à mon établissement", baseComponent: "Canteen" }
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
      if (this.canteen.productionType === "site") {
        return false
      } else if (this.isSatellite) {
        if (this.isApproTab) return !!this.centralDiagnostic
        if (this.centralDiagnostic?.centralKitchenDiagnosticMode === "ALL") {
          return !!this.centralDiagnostic
        }
      } else {
        // both CC production types
        if (!this.isApproTab) {
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
    modificationLink() {
      return this.isCanteenTab
        ? { name: "CanteenForm", params: { canteenUrlComponent: this.canteenUrlComponent } }
        : {
            name: "DiagnosticTunnel",
            params: {
              canteenUrlComponent: this.canteenUrlComponent,
              year: this.year,
              measureId: this.measureId,
            },
          }
    },
    hasCentralDiagnosticForMeasure() {
      if (!this.centralDiagnostic) return false
      if (this.isCanteenTab) return false
      if (this.isApproTab) return true
      return this.centralDiagnostic.centralKitchenDiagnosticMode === "ALL"
    },
    displayDiagnostic() {
      return this.hasCentralDiagnosticForMeasure ? this.centralDiagnostic : this.diagnostic
    },
    showPurchasesSection() {
      const isCurrentYear = this.year === lastYear() + 1
      const managesOwnPurchases = !this.isSatellite
      const dataProvidedByDiagnostic = this.diagnostic && hasDiagnosticApproData(this.diagnostic)
      return this.isApproTab && isCurrentYear && managesOwnPurchases && !dataProvidedByDiagnostic
    },
    hasData() {
      const hasMeasureData = hasStartedMeasureTunnel(this.displayDiagnostic, this.keyMeasure)
      return this.showPurchasesSection || hasMeasureData
    },
    showIntroduction() {
      return !(this.isCanteenTab || this.hasData || this.usesOtherDiagnosticForMeasure)
    },
    showSynthesis() {
      return this.isCanteenTab || this.hasData
    },
  },
  methods: {
    startTunnel() {
      if (this.usesOtherDiagnosticForMeasure) return // more explicit error?
      if (this.diagnostic) {
        this.$router.push(this.modificationLink)
      } else {
        this.requestOngoing = true
        return this.$store
          .dispatch("createDiagnostic", {
            canteenId: this.canteen.id,
            payload: {
              year: this.year,
              creationSource: "TUNNEL",
            },
          })
          .then(() => {
            this.$router.push(this.modificationLink)
          })
          .catch((e) => {
            this.$store.dispatch("notifyServerError", e)
          })
          .finally(() => (this.requestOngoing = false))
      }
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
