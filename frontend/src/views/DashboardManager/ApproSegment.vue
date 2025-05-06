<template>
  <div class="fill-height">
    <v-card
      :to="{
        name: 'MyProgress',
        params: {
          canteenUrlComponent: this.canteenUrlComponent,
          year: this.diagnostic.year,
          measure: 'qualite-des-produits',
        },
      }"
      v-if="hasCentralKitchen"
      outlined
      class="fill-height d-flex flex-column dsfr pa-6"
    >
      <v-card-title>
        <v-icon small :color="keyMeasure.mdiIconColor" class="mx-2">
          {{ keyMeasure.mdiIcon }}
        </v-icon>
        <h3 class="font-weight-bold fr-text">{{ keyMeasure.shortTitle }}</h3>
      </v-card-title>
      <v-card-text v-if="!delegatedToCentralKitchen">
        <KeyMeasureBadge
          class="py-0 ml-8"
          :canteen="canteen"
          :diagnostic="canteenDiagnostic"
          :year="year"
          id="qualite-des-produits"
        />
      </v-card-text>
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
            Les données d’approvisionnement apparaîtront directement ici lorsque votre livreur des repas les aura
            renseignées.
          </p>
          <p v-if="!diagnostic || diagnostic.centralKitchenDiagnosticMode !== 'ALL'">
            En attendant, déclarez vos actions concernant les autres volets de la loi EGalim.
          </p>
        </div>
        <div v-else>
          <ApproGraph :diagnostic="diagnostic" :canteen="canteen" />
        </div>
        <v-spacer />
      </v-card-text>
      <v-spacer></v-spacer>
      <v-card-actions class="px-4">
        <v-spacer></v-spacer>
        <v-icon color="primary" class="mr-n1">$arrow-right-line</v-icon>
      </v-card-actions>
    </v-card>
    <v-card
      :to="{
        name: 'MyProgress',
        params: {
          canteenUrlComponent: this.canteenUrlComponent,
          year: this.diagnostic.year,
          measure: 'qualite-des-produits',
        },
      }"
      outlined
      class="fill-height d-flex flex-column dsfr pa-6"
      v-else-if="diagnostic"
    >
      <v-card-title>
        <v-icon small :color="keyMeasure.mdiIconColor" class="mx-2">
          {{ keyMeasure.mdiIcon }}
        </v-icon>
        <h3 class="fr-text font-weight-bold">{{ keyMeasure.shortTitle }}</h3>
      </v-card-title>
      <v-card-text>
        <KeyMeasureBadge
          class="py-0 ml-8"
          :canteen="canteen"
          :diagnostic="canteenDiagnostic"
          :year="year"
          id="qualite-des-produits"
        />
      </v-card-text>
      <v-card-text v-if="level" :class="`mt-n4 pl-12 py-0 ${level.colorClass}`">
        <p class="mb-0 mt-2 fr-text-xs">
          NIVEAU :
          <span class="font-weight-black">{{ level.text }}</span>
        </p>
      </v-card-text>
      <v-card-text class="fr-text-xs" v-if="hasApproData">
        <ApproGraph :diagnostic="diagnostic" :canteen="canteen" />
        <p class="mb-0">
          Composer des repas avec au moins {{ sustainablePercent }} % de produits de qualité et durables, dont
          {{ bioPercent }} % de bio, pour proposer une alimentation plus saine et écologique à vos convives.
        </p>
      </v-card-text>
      <v-card-text v-else class="fr-text-xs">
        <p>
          Renseignez la valeur (en € HT) de vos achats alimentaires total pour voir la synthèse de vos données.
        </p>
      </v-card-text>
      <v-spacer></v-spacer>
      <v-card-actions class="px-4">
        <v-spacer></v-spacer>
        <v-icon color="primary" class="mr-n1">$arrow-right-line</v-icon>
      </v-card-actions>
    </v-card>
    <div v-else-if="isTdYear" class="fr-text fill-height d-flex flex-column justify-center">
      <p><b>C’est le moment de se lancer !</b></p>
      <p>
        Réalisez un bilan complet pour mesurer votre avancée par rapport aux objectifs de la loi EGalim, et parcourez
        des ressources personnalisées selon votre situation et vos résultats pour vous aider dans votre transition vers
        une alimentation plus durable.
      </p>
    </div>
    <v-card outlined class="fill-height d-flex flex-column dsfr pa-6" v-else-if="isCurrentYear">
      <v-card-title>
        <v-icon small :color="keyMeasure.mdiIconColor" class="mx-2">
          {{ keyMeasure.mdiIcon }}
        </v-icon>
        <h3 class="font-weight-bold fr-text">{{ keyMeasure.shortTitle }}</h3>
      </v-card-title>
      <v-card-text class="fill-height mt-2">
        <div class="overlay d-flex flex-column align-center justify-center fill-height pa-6">
          <p class="fr-text text-center my-10">
            Avec l’outil de suivi d’achats, pilotez en temps réel votre progression EGalim sur l’année en cours, et
            simplifiez votre prochaine télédéclaration.
          </p>
          <v-btn v-if="!hasPurchases" large class="mb-10" color="primary" :to="{ name: 'PurchasesHome' }">
            <span class="fr-text-lg">Commencer</span>
          </v-btn>
          <v-btn v-else outlined large class="mb-10" color="primary" :to="{ name: 'PurchasesHome' }">
            <span class="fr-text-lg">Gérer mes achats</span>
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
    <div v-else class="fr-text fill-height d-flex flex-column justify-center">
      <p><b>Allez plus loin</b></p>
      <p>
        Réalisez un bilan pour communiquer votre progrès auprès vos convives avec votre affiche en ligne.
      </p>
    </div>
  </div>
</template>
<script>
import {
  hasDiagnosticApproData,
  lastYear,
  hasStartedMeasureTunnel,
  applicableDiagnosticRules,
  delegatedToCentralKitchen,
} from "@/utils"
import Constants from "@/constants"
import ApproGraph from "@/components/ApproGraph"
import KeyMeasureBadge from "@/components/KeyMeasureBadge"
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "ApproSegment",
  components: { ApproGraph, KeyMeasureBadge },
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
    canteenDiagnostic: {
      type: Object,
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
    isTdYear() {
      return this.year === this.lastYear
    },
    level() {
      if (this.delegatedToSatellite) return null
      if (!hasStartedMeasureTunnel(this.diagnostic, this.keyMeasure)) return Constants.Levels.UNKNOWN
      return null
    },
    hasPurchases() {
      return false
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
    hasCentralKitchen() {
      if (this.canteen.productionType !== "site_cooked_elsewhere") return false
      return this.diagnostic && this.diagnostic.canteenId === this.canteen.centralKitchen?.id
    },
    centralKitchenDisplayName() {
      if (this.canteen.centralKitchen?.name) {
        return this.canteen.centralKitchen.name
      }
      return this.canteen.centralProducerSiret
        ? `l'établissement avec le SIRET ${this.canteen.centralProducerSiret}`
        : "un établissement inconnu"
    },
    rules() {
      return applicableDiagnosticRules(this.canteen)
    },
    sustainablePercent() {
      return this.rules.qualityThreshold
    },
    bioPercent() {
      return this.rules.bioThreshold
    },
    delegatedToCentralKitchen() {
      return delegatedToCentralKitchen(this.canteen, this.diagnostic)
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
