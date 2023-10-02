<template>
  <v-row style="position: relative;">
    <v-col cols="12" md="4" class="d-flex flex-column">
      <v-row>
        <v-col cols="7">
          <h2 class="fr-h5 mb-0 mt-1 align-center">
            Ma progression
          </h2>
        </v-col>
        <v-col cols="5">
          <DsfrSelect v-model="year" :items="allowedYears" hide-details="auto" placeholder="Année" />
        </v-col>
      </v-row>
      <div>
        <MissingDataChip v-if="!hasPurchases && !diagnostic && !hasLastYearDiagnostic" class="mt-4" />
        <v-divider class="my-6"></v-divider>
      </div>
      <ApproSegment :purchases="null" :diagnostic="diagnostic" :lastYearDiagnostic="null" :canteen="canteen" />
    </v-col>
    <v-col cols="12" md="8">
      <v-row style="position: relative;">
        <div
          class="overlay d-flex align-center justify-center"
          v-if="!hasPurchases && !diagnostic && !hasLastYearDiagnostic"
        >
          <v-btn
            color="primary"
            :to="{
              name: !diagnostic ? 'NewDiagnosticForCanteen' : 'DiagnosticModification',
              params: { canteenUrlComponent, year: diagnostic && year },
              query: { année: year },
            }"
          >
            Commencer
          </v-btn>
        </div>
        <v-col cols="12" md="6" fill-height>
          <FoodWasteCard :diagnostic="diagnostic" :canteen="canteen" />
        </v-col>
        <v-col cols="12" md="6" fill-height>
          <DiversificationCard :diagnostic="diagnostic" :canteen="canteen" />
        </v-col>
        <v-col cols="12" md="6" fill-height>
          <NoPlasticCard :diagnostic="diagnostic" :canteen="canteen" />
        </v-col>
        <v-col cols="12" md="6" fill-height>
          <InformationCard :diagnostic="diagnostic" :canteen="canteen" />
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import DsfrSelect from "@/components/DsfrSelect"
import { lastYear, diagnosticYears } from "@/utils"
import FoodWasteCard from "./FoodWasteCard"
import DiversificationCard from "./DiversificationCard"
import NoPlasticCard from "./NoPlasticCard"
import InformationCard from "./InformationCard"
import MissingDataChip from "./MissingDataChip"
import ApproSegment from "./ApproSegment"

export default {
  name: "EgalimProgression",
  components: {
    DsfrSelect,
    FoodWasteCard,
    DiversificationCard,
    NoPlasticCard,
    InformationCard,
    MissingDataChip,
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
    diagnostic() {
      return this.canteen.diagnostics.find((x) => x.year === this.year)
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
  },
}
</script>

<style scoped>
.overlay {
  position: absolute;
  top: 4%;
  left: 3%;
  z-index: 1;
  background: #bbbbbb50;
  width: 94%;
  height: 92%;
  backdrop-filter: blur(7px);
  border: dashed #bbb;
}
</style>
