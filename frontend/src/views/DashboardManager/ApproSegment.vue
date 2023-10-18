<template>
  <div class="fill-height">
    <v-card v-if="hasCentralKitchen" outlined class="fill-height d-flex flex-column dsfr pa-6">
      <v-card-title>
        <v-icon small :color="keyMeasure.mdiIconColor" class="mx-2">
          {{ keyMeasure.mdiIcon }}
        </v-icon>
        <h3 class="font-weight-bold fr-text">{{ keyMeasure.shortTitle }}</h3>
      </v-card-title>
      <v-card-text class="fill-height d-flex flex-column" style="position: relative;">
        <v-spacer />
        <v-card class="py-4 px-5" color="grey lighten-4">
          <p class="mb-0 grey--text text--darken-2">
            Votre cantine sert des repas préparés par
            <strong>{{ centralKitchenDisplayName }}</strong>
          </p>
        </v-card>
        <v-spacer />
        <div v-if="!hasApproData">
          <p>
            Les données d’approvisionnement apparaîtront directement ici lorsque votre cuisine centrale les aura
            renseignées.
          </p>
          <p v-if="!diagnostic || diagnostic.centralKitchenDiagnosticMode !== 'ALL'">
            En attendant, déclarez vos actions concernant les autres volets de la loi EGAlim.
          </p>
        </div>
        <div v-else>
          <ApproGraph :diagnostic="diagnostic" :canteen="canteen" />
        </div>
        <v-spacer />
      </v-card-text>
    </v-card>
    <div v-else-if="showFirstTimeView" class="body-1">
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
    <v-card outlined class="fill-height d-flex flex-column dsfr pa-6" v-else-if="!hasApproData && isCurrentYear">
      <v-card-title>
        <v-icon small :color="keyMeasure.mdiIconColor" class="mx-2">
          {{ keyMeasure.mdiIcon }}
        </v-icon>
        <h3 class="font-weight-bold fr-text">{{ keyMeasure.shortTitle }}</h3>
      </v-card-title>
      <v-card-text class="fill-height mt-2">
        <div class="overlay d-flex flex-column align-center justify-center fill-height pa-6">
          <p class="fr-text text-center my-10">
            Avec l’outil de suivi d’achats, pilotez en temps réel votre progression EGAlim sur l’année en cours, et
            simplifiez votre prochaine télédéclaration.
          </p>
          <v-btn large class="mb-10" color="primary" :to="{ name: 'PurchasesHome' }">
            <span class="fr-text-lg">Commencer</span>
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
    <v-card :to="link" outlined class="fill-height d-flex flex-column dsfr pa-6" v-else-if="diagnostic">
      <v-card-title>
        <v-icon small :color="keyMeasure.mdiIconColor" class="mx-2">
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
    year: {
      type: Number,
    },
  },
  data() {
    return {
      lastYear: lastYear(),
    }
  },
  computed: {
    keyMeasure() {
      return keyMeasures.find((x) => x.id === "qualite-des-produits")
    },
    hasApproData() {
      return this.diagnostic && hasDiagnosticApproData(this.diagnostic)
    },
    isCurrentYear() {
      return this.year === this.lastYear + 1
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
      return !!this.lastYearDiagnostic
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
    hasCentralKitchen() {
      if (this.canteen.productionType !== "site_cooked_elsewhere") return false
      return !!this.canteen.centralKitchen?.id
    },
    centralKitchenDisplayName() {
      if (this.canteen.centralKitchen?.name) {
        return this.canteen.centralKitchen.name
      }
      return this.canteen.centralProducerSiret
        ? `l'établissement avec le SIRET ${this.canteen.centralProducerSiret}`
        : "un établissement inconnu"
    },
    link() {
      return this.diagnostic
        ? {
            name: "MyProgress",
            params: {
              canteenUrlComponent: this.canteenUrlComponent,
              year: this.diagnostic.year,
              measure: "qualite-des-produits",
            },
          }
        : null
    },
  },
}
</script>

<style scoped>
.overlay {
  background: #f5f5fe;
  backdrop-filter: blur(7px);
  border: 1.5px dashed #000091;
  border-radius: 5px;
  color: #3a3a3a;
}
.v-card.dsfr {
  border: solid 1.5px #dddddd;
}
</style>
