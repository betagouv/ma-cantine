<template>
  <div class="fill-height">
    <div v-if="showFirstTimeView" class="body-1">
      <p class="font-weight-bold">Pilotez votre progression tout au long de l’année en cours</p>
      <p class="body-2">
        Avec l’outil de suivi d’achats de « ma cantine », calculez automatiquement et en temps réel la part de vos
        approvisionnements qui correspondent aux critères de la loi EGAlim, et facilitez ainsi votre prochaine
        télédéclaration.
      </p>
      <p class="body-2">
        Pour cela, vous pouvez renseigner tous vos achats au fil de l’eau ou par import en masse, ou bien connecter
        votre outil de gestion habituel si cela est possible pour transférer les données.
      </p>
    </div>
    <v-card outlined class="fill-height d-flex flex-column" v-else-if="!hasApproData">
      <v-card-title class="font-weight-bold fr-text">
        <v-icon small :color="keyMeasure.mdiIconColor" class="mr-2">
          {{ keyMeasure.mdiIcon }}
        </v-icon>
        <h3>{{ keyMeasure.shortTitle }}</h3>
      </v-card-title>
      <v-card-text class="fill-height" style="position: relative;">
        <div class="overlay d-flex flex-column align-center justify-center">
          <p class="body-2 pa-4 text-center">
            Avec l’outil de suivi d’achats, pilotez en temps réel votre progression EGAlim sur l’année en cours, et
            simplifiez votre prochaine télédéclaration.
          </p>
          <v-btn
            color="primary"
            :to="{ name: 'DiagnosticModification', params: { canteenUrlComponent, year: diagnostic.year } }"
          >
            Commencer
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
    <v-card
      :to="{ name: 'DiagnosticModification', params: { canteenUrlComponent, year: diagnostic.year } }"
      outlined
      class="fill-height d-flex flex-column dsfr pa-6"
      v-else-if="diagnostic"
    >
      <v-card-title class="mx-1">
        <v-icon small :color="keyMeasure.mdiIconColor" class="mr-2">
          {{ keyMeasure.mdiIcon }}
        </v-icon>
        <h3 class="fr-text font-weight-bold">{{ keyMeasure.shortTitle }}</h3>
      </v-card-title>
      <v-card-text :class="`mt-n4 pl-12 py-0 ${level.colorClass}`">
        <p class="mb-0 mt-2 fr-text-xs">
          NIVEAU :
          <span class="font-weight-black">{{ level.text }}</span>
        </p>
      </v-card-text>
      <v-card-text class="fr-text-xs">
        <ApproGraph :diagnostic="diagnostic" :canteen="canteen" />
        <p>
          C’est parti ! Découvrez les outils et les ressources personnalisées pour vous aider à atteindre un des deux
          objectifs EGAlim et passer au niveau suivant !
        </p>
      </v-card-text>
      <v-spacer></v-spacer>
      <v-card-actions class="px-4">
        <v-spacer></v-spacer>
        <v-icon color="primary" class="mr-n1">$arrow-right-line</v-icon>
      </v-card-actions>
    </v-card>
  </div>
</template>
<script>
import { hasDiagnosticApproData, lastYear } from "@/utils"
import Constants from "@/constants"
import ApproGraph from "./ApproGraph"
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "ApproSegment",
  components: { ApproGraph },
  props: {
    purchases: {
      type: Array,
    },
    diagnostic: {
      type: Object,
    },
    canteen: {
      type: Object,
      required: true,
    },
    lastYearDiagnostic: {
      type: Object,
    },
  },
  computed: {
    keyMeasure() {
      return keyMeasures.find((x) => x.id === "qualite-des-produits")
    },
    hasApproData() {
      return this.diagnostic && hasDiagnosticApproData(this.diagnostic)
    },
    isCurrentYear() {
      return this.diagnostic.year === lastYear() + 1
    },
    level() {
      return Constants.Levels.BEGINNER
    },
    showFirstTimeView() {
      return !this.hasPurchases && !this.diagnostic && !this.hasLastYearDiagnostic
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
