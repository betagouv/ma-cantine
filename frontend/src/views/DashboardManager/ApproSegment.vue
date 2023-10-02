<template>
  <div class="fill-height">
    <div v-if="showFirstTimeView" class="body-1">
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
    <v-card outlined class="fill-height d-flex flex-column" v-else-if="!hasApproData">
      <v-card-title class="font-weight-bold body-1">
        <v-icon color="red" class="mr-2">
          mdi-food-apple
        </v-icon>
        <span>Qualité des produits</span>
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
      class="fill-height d-flex flex-column dsfr"
      v-else-if="diagnostic"
    >
      <v-card-title class="font-weight-bold body-1">
        <v-icon color="red" class="mr-2">
          mdi-food-apple
        </v-icon>
        <span>Qualité des produits</span>
      </v-card-title>
      <v-card-text :class="`mt-n4 pl-12 py-0 ${level.colorClass}`">
        NIVEAU :
        <span class="font-weight-bold">{{ level.text }}</span>
      </v-card-text>
      <v-card-text>
        <ApproGraph :diagnostic="diagnostic" :canteen="canteen" />
        <p class="body-2">
          C’est parti ! Découvrez les outils et les ressources personnalisées pour vous aider à atteindre un des deux
          objectifs EGAlim et passer au niveau suivant !
        </p>
      </v-card-text>
      <v-spacer></v-spacer>
      <v-card-actions class="px-4 pt-0">
        <v-spacer></v-spacer>
        <v-icon color="primary">$arrow-right-line</v-icon>
      </v-card-actions>
    </v-card>
  </div>
</template>
<script>
import { hasDiagnosticApproData, lastYear } from "@/utils"
import Constants from "@/constants"
import ApproGraph from "./ApproGraph.vue"

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
    },
    lastYearDiagnostic: {
      type: Object,
    },
  },
  computed: {
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
