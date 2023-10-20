<template>
  <v-row style="position: relative;">
    <v-col cols="12" md="4" class="d-flex flex-column">
      <v-row>
        <v-col cols="8">
          <h2 class="fr-h3 mb-0 mt-1 align-center">
            Ma progression
          </h2>
        </v-col>
        <v-col cols="4">
          <DsfrSelect v-model="year" :items="allowedYears" hide-details="auto" placeholder="Année" />
        </v-col>
      </v-row>
      <div>
        <DataInfoBadge
          :currentYear="isCurrentYear"
          :missingData="needsData"
          :readyToTeledeclare="readyToTeledeclare"
          class="mt-4"
        />
        <hr aria-hidden="true" role="presentation" class="my-6" />
      </div>
      <ApproSegment :purchases="null" :diagnostic="approDiagnostic" :lastYearDiagnostic="null" :canteen="canteen" />
    </v-col>
    <v-col cols="12" md="8">
      <v-row style="position: relative; height: 100%" class="ma-0">
        <div
          class="overlay d-flex align-center justify-center"
          v-if="!hasPurchases && !otherMeasuresDiagnostic && !hasLastYearDiagnostic"
        >
          <!-- TODO: for satellites who have APPRO declared for them, skip to gaspi tab -->
          <v-btn
            large
            color="primary"
            :to="{
              name: 'MyProgress',
              params: { canteenUrlComponent, year: year, measure: 'qualite-des-produits' },
            }"
          >
            <span class="fr-text-lg">Commencer</span>
          </v-btn>
        </div>
        <v-col cols="12" md="6" class="pt-md-0">
          <FoodWasteCard :diagnostic="otherMeasuresDiagnostic" :canteen="canteen" />
        </v-col>
        <v-col cols="12" md="6" class="pt-md-0">
          <DiversificationCard :diagnostic="otherMeasuresDiagnostic" :canteen="canteen" />
        </v-col>
        <v-col cols="12" md="6" class="pb-md-0">
          <NoPlasticCard :diagnostic="otherMeasuresDiagnostic" :canteen="canteen" />
        </v-col>
        <v-col cols="12" md="6" class="pb-md-0">
          <InformationCard :diagnostic="otherMeasuresDiagnostic" :canteen="canteen" />
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import DsfrSelect from "@/components/DsfrSelect"
import { lastYear, diagnosticYears, hasDiagnosticApproData } from "@/utils"
import FoodWasteCard from "./FoodWasteCard"
import DiversificationCard from "./DiversificationCard"
import NoPlasticCard from "./NoPlasticCard"
import InformationCard from "./InformationCard"
import DataInfoBadge from "./DataInfoBadge"
import ApproSegment from "./ApproSegment"

export default {
  name: "EgalimProgression",
  components: {
    DsfrSelect,
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
    return {
      year: lastYear(),
      allowedYears: diagnosticYears().map((year) => ({ text: year, value: year })),
    }
  },
  computed: {
    canteenDiagnostic() {
      return this.canteen.diagnostics.find((x) => x.year === this.year)
    },
    centralDiagnostic() {
      if (this.canteen.productionType === "site_cooked_elsewhere") {
        const ccDiag = this.canteen.centralKitchenDiagnostics?.find((x) => x.year === this.year)
        return ccDiag
      }
      return null
    },
    approDiagnostic() {
      return this.centralDiagnostic || this.canteenDiagnostic
    },
    otherMeasuresDiagnostic() {
      if (this.centralDiagnostic?.centralKitchenDiagnosticMode === "ALL") {
        return this.centralDiagnostic
      }
      return this.canteenDiagnostic
    },
    hasPurchases() {
      return false
    },
    hasLastYearDiagnostic() {
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
        !this.hasPurchases && (!this.approDiagnostic || !this.otherMeasuresDiagnostic) && !this.hasLastYearDiagnostic
      )
    },
    readyToTeledeclare() {
      const inTdCampaign = window.ENABLE_TELEDECLARATION && this.year === lastYear()
      if (!inTdCampaign) return false
      if (this.centralDiagnostic) {
        const noNeedToTd = this.centralDiagnostic.centralKitchenDiagnosticMode === "ALL"
        const requiresOtherData = !noNeedToTd
        const hasOtherData = !!this.canteenDiagnostic
        return requiresOtherData && hasOtherData
      }
      return this.canteenDiagnostic && hasDiagnosticApproData(this.canteenDiagnostic)
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
</style>
