<template>
  <v-row>
    <v-col cols="12" md="4">
      <v-row>
        <v-col cols="7">
          <h2 class="fr-h5 mb-0 mt-1 align-center">
            Ma progression
          </h2>
        </v-col>
        <v-col cols="5">
          <DsfrSelect ref="yearSelect" v-model="year" :items="allowedYears" hide-details="auto" placeholder="Année" />
        </v-col>
      </v-row>
      <MissingDataChip v-if="!hasPurchases && !hasCurrentDiagnostic && !hasLastYearDiagnostic" class="mt-4 mb-n2" />
      <v-divider class="my-6"></v-divider>
      <ApproSegment :purchases="null" :currentDiagnostic="null" :lastYearDiagnostic="null" />
    </v-col>
    <v-col cols="12" md="8">
      <v-row style="position: relative;">
        <div
          class="overlay d-flex align-center justify-center"
          v-if="!hasPurchases && !hasCurrentDiagnostic && !hasLastYearDiagnostic"
        >
          <v-btn color="primary">Commencer</v-btn>
        </div>
        <v-col cols="12" md="6" fill-height>
          <FoodWasteCard />
        </v-col>
        <v-col cols="12" md="6" fill-height>
          <DiversificationCard />
        </v-col>
        <v-col cols="12" md="6" fill-height>
          <NoPlasticCard />
        </v-col>
        <v-col cols="12" md="6" fill-height>
          <InformationCard />
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import DsfrSelect from "@/components/DsfrSelect"
import { lastYear, diagnosticYears } from "@/utils"
import FoodWasteCard from "./FoodWasteCard.vue"
import DiversificationCard from "./DiversificationCard.vue"
import NoPlasticCard from "./NoPlasticCard.vue"
import InformationCard from "./InformationCard.vue"
import MissingDataChip from "./MissingDataChip.vue"
import ApproSegment from "./ApproSegment.vue"

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
  data() {
    return {
      year: lastYear(),
      allowedYears: diagnosticYears().map((year) => ({ text: year, value: year })),
    }
  },
  computed: {
    hasPurchases() {
      return false
    },
    hasCurrentDiagnostic() {
      return false
    },
    hasLastYearDiagnostic() {
      return false
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
