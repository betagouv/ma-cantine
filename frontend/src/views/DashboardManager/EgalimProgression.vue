<template>
  <div>
    <v-row style="position: relative;">
      <v-col cols="12" md="4" class="d-flex flex-column">
        <v-row>
          <v-col cols="12" sm="8">
            <h2 class="fr-h3 mb-0 mt-1 align-center">
              Mon bilan annuel
            </h2>
          </v-col>
          <v-col>
            <DsfrNativeSelect v-model="selectedYear" :items="allowedYears" label="Année" labelClasses="d-sr-only" />
          </v-col>
        </v-row>
        <div>
          <DataInfoBadge
            :currentYear="isCurrentYear"
            :missingData="needsData"
            :readyToTeledeclare="readyToTeledeclare"
            :hasActiveTeledeclaration="hasActiveTeledeclaration"
            class="mt-4"
          />
          <DataInfoBadge
            :currentYear="isCurrentYear"
            :missingData="needsData"
            :readyToTeledeclare="readyToTeledeclare"
            :hasActiveTeledeclaration="hasActiveTeledeclaration"
            :canteenAction="canteenAction"
            class="mt-4"
          />
          <hr aria-hidden="true" role="presentation" class="my-6" />
        </div>
        <ApproSegment
          :purchases="null"
          :diagnostic="approDiagnostic"
          :lastYearDiagnostic="lastYearDiagnostic"
          :canteen="canteen"
          :year="year"
        />
      </v-col>
      <v-col cols="12" md="8">
        <v-row style="position: relative; height: 100%" class="ma-0">
          <div class="overlay d-flex align-center justify-center" v-if="!otherMeasuresDiagnostic">
            <v-btn
              large
              color="primary"
              :to="{
                name: 'MyProgress',
                params: { canteenUrlComponent, year: year, measure: firstActionableMeasure },
              }"
            >
              <span class="fr-text-lg">Faire le bilan {{ year }}</span>
            </v-btn>
          </div>
          <v-col cols="12" md="6" class="pt-md-0 px-0 pr-md-3">
            <FoodWasteCard :diagnostic="otherMeasuresDiagnostic" :canteen="canteen" />
          </v-col>
          <v-col cols="12" md="6" class="pt-md-0 px-0 pl-md-3">
            <DiversificationCard :diagnostic="otherMeasuresDiagnostic" :canteen="canteen" />
          </v-col>
          <v-col cols="12" md="6" class="pb-md-0 px-0 pr-md-3">
            <NoPlasticCard :diagnostic="otherMeasuresDiagnostic" :canteen="canteen" />
          </v-col>
          <v-col cols="12" md="6" class="pb-md-0 px-0 pl-md-3">
            <InformationCard :diagnostic="otherMeasuresDiagnostic" :canteen="canteen" />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-card v-if="missingCanteenData" class="pa-6 my-6 fr-text grey--text text--darken-3 text-center cta-block">
      <p>
        Certaines données de votre établissement manquent.
        <span v-if="inTeledeclarationCampaign">
          Veuillez compléter ces informations avant télédéclarer.
        </span>
      </p>
      <v-card-actions class="px-0 pt-0 pb-0 justify-center">
        <v-btn :to="{ name: 'CanteenForm' }" color="primary" class="fr-text font-weight-medium">
          Mettre à jour mon établissement
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-card
      v-else-if="hasSatelliteInconsistency"
      class="pa-6 my-6 fr-text grey--text text--darken-3 text-center cta-block"
    >
      <p>
        {{ satelliteInconsistencyMessage }}
        <span v-if="inTeledeclarationCampaign">
          Veuillez corriger le divergence avant télédéclarer.
        </span>
      </p>
      <v-card-actions class="px-0 pt-0 pb-0 justify-center">
        <v-btn :to="{ name: 'SatelliteManagement' }" color="primary" class="fr-text font-weight-medium">
          Gérer mes satellites
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-card
      v-else-if="diagnosticCanBeTeledeclared"
      class="pa-6 pb-2 pb-sm-6 my-6 fr-text grey--text text--darken-3 text-center cta-block"
    >
      <div v-if="tunnelComplete">
        <p class="mb-0">
          Votre bilan {{ canteenDiagnostic.year }} est complet ! Merci d’avoir pris le temps de saisir vos données !
        </p>
        <p>
          Vérifiez-les une dernière fois et télédéclarez-les pour participer au bilan statistique national obligatoire.
        </p>
      </div>
      <div v-else>
        <p class="mb-0">{{ tunnelProgressMessage }}</p>
        <p>
          Completez votre bilan, ou télédéclarez seulement ces données.
        </p>
      </div>
      <v-card-actions class="px-0 pt-0 pb-0 justify-center flex-wrap">
        <v-btn v-if="!tunnelComplete" color="primary" :to="completeDiagnosticLink" class="mb-4 mb-sm-0">
          Complèter mon bilan
        </v-btn>
        <v-btn
          color="primary"
          :outlined="!tunnelComplete"
          @click="showTeledeclarationPreview = true"
          class="fr-text font-weight-medium mb-4 mb-sm-0"
        >
          Vérifier et télédéclarer mes données {{ canteenDiagnostic.year }}
        </v-btn>
      </v-card-actions>
    </v-card>
    <TeledeclarationPreview
      v-if="canteenDiagnostic"
      :diagnostic="canteenDiagnostic"
      :canteen="canteen"
      v-model="showTeledeclarationPreview"
      @teledeclare="submitTeledeclaration"
    />
  </div>
</template>

<script>
import DsfrNativeSelect from "@/components/DsfrNativeSelect"
import TeledeclarationPreview from "@/components/TeledeclarationPreview"
import {
  lastYear,
  customDiagnosticYears,
  readyToTeledeclare,
  diagnosticCanBeTeledeclared,
  inTeledeclarationCampaign,
  missingCanteenData,
  hasSatelliteInconsistency,
  hasFinishedMeasureTunnel,
} from "@/utils"
import FoodWasteCard from "./FoodWasteCard"
import DiversificationCard from "./DiversificationCard"
import NoPlasticCard from "./NoPlasticCard"
import InformationCard from "./InformationCard"
import DataInfoBadge from "@/components/DataInfoBadge"
import ApproSegment from "./ApproSegment"

export default {
  name: "EgalimProgression",
  components: {
    DsfrNativeSelect,
    TeledeclarationPreview,
    FoodWasteCard,
    DiversificationCard,
    NoPlasticCard,
    InformationCard,
    DataInfoBadge,
    ApproSegment,
  },
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  data() {
    const years = customDiagnosticYears(this.canteen.diagnostics)
    return {
      lastYear: lastYear(),
      selectedYear: lastYear(),
      diagnosticYears: years,
      allowedYears: years.map((year) => ({ text: year, value: year })),
      showTeledeclarationPreview: false,
      purchasesSummary: undefined,
      canteenAction: null,
    }
  },
  computed: {
    year() {
      return +this.selectedYear
    },
    canteenDiagnostic() {
      return this.canteen.diagnostics.find((x) => x.year === this.year)
    },
    hasActiveTeledeclaration() {
      return this.canteenDiagnostic?.teledeclaration?.status === "SUBMITTED"
    },
    lastYearDiagnostic() {
      return this.canteen.diagnostics.find((x) => x.year === this.lastYear)
    },
    centralDiagnostic() {
      if (this.canteen.productionType === "site_cooked_elsewhere") {
        const ccDiag = this.canteen.centralKitchenDiagnostics?.find((x) => x.year === this.year)
        return ccDiag
      }
      return null
    },
    approDiagnostic() {
      if (this.isCurrentYear && this.purchasesSummary && this.purchasesSummary.valueTotalHt !== 0) {
        return this.purchasesSummary
      }
      return this.centralDiagnostic || this.canteenDiagnostic
    },
    otherMeasuresDiagnostic() {
      if (this.centralDiagnostic?.centralKitchenDiagnosticMode === "ALL") {
        return this.centralDiagnostic
      }
      return this.canteenDiagnostic
    },
    firstActionableMeasure() {
      if (
        this.canteen.productionType === "site_cooked_elsewhere" &&
        this.centralDiagnostic?.centralKitchenDiagnosticMode === "APPRO"
      ) {
        return "gaspillage-alimentaire"
      }
      return "qualite-des-produits"
    },
    hasPurchases() {
      return false
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
    isCurrentYear() {
      return this.year === lastYear() + 1
    },
    needsData() {
      return (
        (!this.hasPurchases && (!this.approDiagnostic || !this.otherMeasuresDiagnostic)) ||
        !this.diagnosticCanBeTeledeclared
      )
    },
    diagnosticCanBeTeledeclared() {
      return diagnosticCanBeTeledeclared(this.canteen, this.canteenDiagnostic)
    },
    inTeledeclarationCampaign() {
      return inTeledeclarationCampaign(this.year)
    },
    missingCanteenData() {
      return missingCanteenData(this.canteen, this.$store.state.sectors)
    },
    hasSatelliteInconsistency() {
      return hasSatelliteInconsistency(this.canteen)
    },
    satelliteInconsistencyMessage() {
      const satelliteCount = this.canteen.satelliteCanteensCount
      const declared = satelliteCount === 1 ? `une cantine` : `${satelliteCount} cantines`
      const dbCount = this.canteen.satellites?.length
      const dbString = dbCount === 1 ? "une cantine associée" : `${dbCount} cantines associées`
      return (
        `Vous avez déclaré que votre établissement livrait des repas à ${declared}, ` +
        `mais nous comptons ${dbString} à votre établissement dans notre base de données.`
      )
    },
    readyToTeledeclare() {
      return readyToTeledeclare(this.canteen, this.canteenDiagnostic, this.$store.state.sectors)
    },
    tunnelComplete() {
      return this.canteenDiagnostic && hasFinishedMeasureTunnel(this.canteenDiagnostic)
    },
    tunnelProgressMessage() {
      return "Merci d'avoir pris le temps de commencer votre bilan !"
    },
    completeDiagnosticLink() {
      return {
        name: "MyProgress",
        params: {
          canteenUrlComponent: this.canteenUrlComponent,
          year: this.canteenDiagnostic.year,
          measure: this.firstActionableMeasure,
        },
      }
    },
  },
  methods: {
    replaceDiagnostic(diagnostic) {
      const diagnosticIndex = this.canteen.diagnostics.findIndex((x) => x.id === diagnostic.id)
      if (diagnosticIndex > -1) {
        this.canteen.diagnostics.splice(diagnosticIndex, 1, diagnostic)
      }
    },
    submitTeledeclaration() {
      return this.$store
        .dispatch("submitTeledeclaration", { id: this.canteenDiagnostic.id })
        .then((diagnostic) => {
          this.$store.dispatch("notify", {
            title: "Télédéclaration prise en compte",
            status: "success",
          })
          this.replaceDiagnostic(diagnostic)
          window.scrollTo(0, 0)
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
        .finally(() => {
          this.showTeledeclarationPreview = false
        })
    },
    fetchPurchasesSummary() {
      this.purchasesSummary = null
      if (this.canteen?.id) {
        return fetch(`/api/v1/canteenPurchasesSummary/${this.canteen.id}?year=${this.year}`)
          .then((response) => (response.ok ? response.json() : {}))
          .then((response) => (this.purchasesSummary = response))
          .catch((e) => {
            this.$store.dispatch("notifyServerError", e)
          })
      }
    },
    fetchCanteenAction() {
      fetch(`/api/v1/actionableCanteens/${this.canteen.id}/${this.year}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((canteen) => {
          this.canteenAction = canteen.action
        })
    },
  },
  mounted() {
    if (this.$route.query?.year && this.diagnosticYears.indexOf(+this.$route.query.year) > -1) {
      this.year = +this.$route.query.year
      this.$router.replace({ query: {} })
    }
  },
  watch: {
    year: {
      handler() {
        this.fetchCanteenAction()
        if (this.isCurrentYear && !this.purchasesSummary) {
          this.fetchPurchasesSummary()
        }
      },
      immediate: true,
    },
  },
}
</script>

<style scoped>
.overlay {
  position: absolute;
  top: 4%;
  left: 5%;
  z-index: 1;
  background: rgba(245, 245, 254, 0.2);
  width: 90%;
  height: 92%;
  backdrop-filter: blur(7px);
  border: 1.5px dashed #000091;
  border-radius: 5px;
  color: #3a3a3a;
}
.v-card.dsfr {
  border: solid 1.5px #dddddd;
}
.cta-block {
  background: #f5f5fe;
  backdrop-filter: blur(7px);
  border: 1.5px dashed #000091;
  border-radius: 24px;
  color: #3a3a3a;
}
</style>
