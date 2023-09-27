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
      <v-chip
        outlined
        color="primary"
        small
        label
        v-if="!hasPurchases && !hasCurrentDiagnostic && !hasLastYearDiagnostic"
        class="mt-4 mb-n2"
      >
        <v-icon small class="mr-2">$information-fill</v-icon>
        DONNÉES À COMPLETER
      </v-chip>
      <v-divider class="my-6"></v-divider>
      <div v-if="!hasPurchases && !hasCurrentDiagnostic && !hasLastYearDiagnostic" class="body-1">
        <p class="font-weight-bold">Pilotez votre progression tout au long de l’année en cours</p>
        <p class="body-2">
          Avec l’outil de suivi d’achats de “ma cantine”, calculez automatiquement et en temps réel la part de vos
          approvisionnements qui correspondent aux critères de la loi EGAlim, et facilitez ainsi votre prochaine
          télédéclaration.
        </p>
        <p class="body-2">
          Pour cela, vous pouvez renseigner tous vos achats au fil de l’eau ou par import en masse, ou bien connecter
          votre outil de gestion habituel si cela est possible pour transférer les données.
        </p>
      </div>
    </v-col>
    <v-col cols="12" md="8">
      <v-row style="position: relative;">
        <div
          class="overlay d-flex align-center justify-center"
          v-if="!hasPurchases && !hasCurrentDiagnostic && !hasLastYearDiagnostic && false"
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

export default {
  name: "EgalimProgression",
  components: { DsfrSelect, FoodWasteCard, DiversificationCard, NoPlasticCard, InformationCard },
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
