<template>
  <div class="fr-text-xs" v-if="hasApproData">
    <ApproGraph :diagnostic="diagnostic" :canteen="canteen" aria-hidden="true" />
    <v-row>
      <v-col cols="12" md="6">
        <h5 class="mb-4 font-weight-bold fr-text-sm">Détail du calcul de mes taux EGAlim</h5>
        <v-row>
          <v-col cols="6">
            <p class="mb-0">Produits bio</p>
          </v-col>
          <v-col cols="2">
            <p class="mb-0 font-weight-bold">{{ percentages.bio || "—" }} %</p>
          </v-col>
          <v-col cols="4">
            <p class="mb-0">
              <i>objectif : {{ applicableRules.bioThreshold }} %</i>
            </p>
          </v-col>
        </v-row>
        <v-row class="mt-0">
          <v-col cols="6">
            <p class="mb-0">Produits durables et de qualité (hors bio)</p>
          </v-col>
          <v-col cols="2">
            <p class="mb-0 font-weight-bold">{{ percentages.allSustainable || "—" }} %</p>
          </v-col>
        </v-row>
        <v-row class="mt-1">
          <v-col cols="8">
            <hr aria-hidden="true" role="presentation" />
          </v-col>
        </v-row>
        <v-row class="mt-0">
          <v-col cols="6">
            <p class="mb-0">Produits EGAlim</p>
          </v-col>
          <v-col cols="2">
            <p class="mb-0 font-weight-bold">{{ percentages.egalim || "—" }} %</p>
          </v-col>
          <v-col cols="4">
            <p class="mb-0">
              <i>objectif : {{ applicableRules.qualityThreshold }} %</i>
            </p>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="12" md="6">
        <h5 class="mb-5 font-weight-bold fr-text-sm">Par famille de produits</h5>
        <v-row class="py-2">
          <v-col class="py-0">
            <p class="mb-0">
              <v-icon :small="$vuetify.breakpoint.xs" class="mr-1 mr-sm-2" color="#00A95F">$award-line</v-icon>
              <span class="font-weight-bold percentage">{{ percentages.meatPoultryEgalim || "—" }} %</span>
              de viandes et volailles EGAlim
            </p>
          </v-col>
          <v-col class="py-0" v-if="applicableRules.meatPoultryEgalimThreshold" cols="12" sm="4" md="3">
            <p class="mb-0 grey--text text-darken-1">
              <i>objectif : {{ applicableRules.meatPoultryEgalimThreshold }} %</i>
            </p>
          </v-col>
        </v-row>
        <v-row class="py-2">
          <v-col class="py-0">
            <p class="mb-0">
              <v-icon :small="$vuetify.breakpoint.xs" class="mr-1 mr-sm-2" color="#00A95F">$france-line</v-icon>
              <span class="font-weight-bold percentage">{{ percentages.meatPoultryFrance || "—" }} %</span>
              de viandes et volailles provenance France
            </p>
          </v-col>
          <v-col class="py-0" v-if="applicableRules.meatPoultryFranceThreshold" cols="12" sm="4" md="3">
            <p class="mb-0 grey--text text-darken-1">
              <i>objectif : {{ applicableRules.meatPoultryFranceThreshold }} %</i>
            </p>
          </v-col>
        </v-row>
        <v-row class="py-2">
          <v-col class="py-0">
            <p class="mb-0">
              <v-icon :small="$vuetify.breakpoint.xs" class="mr-1 mr-sm-2" color="#00A95F">$anchor-line</v-icon>
              <span class="font-weight-bold percentage">{{ percentages.fishEgalim || "—" }} %</span>
              de produits de la mer et aquaculture EGAlim
            </p>
          </v-col>
          <v-col class="py-0" v-if="applicableRules.fishEgalimThreshold" cols="12" sm="4" md="3">
            <p class="mb-0 grey--text text-darken-1">
              <i>objectif : {{ applicableRules.fishEgalimThreshold }} %</i>
            </p>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <DsfrAccordion
      v-if="!usesCentralDiagnostic"
      class="mt-10"
      :items="[{ title: 'Données détaillées', titleLevel: 'h5' }]"
    >
      <template v-slot:content>
        <QualityDiagnosticValue
          v-for="(field, idx) in totalFields"
          :key="`total-${idx}`"
          :text="field.text"
          :value="diagnostic[field.key]"
        />
        <div class="my-8">
          <QualityDiagnosticValue
            text="Mode de saisie des données"
            :value="isDetailedDiagnostic ? 'Détaillée' : 'Simplifiée'"
          />
        </div>
        <div class="my-8">
          <QualityDiagnosticValue
            v-for="(field, idx) in egalimFields"
            :key="`egalim-${idx}`"
            :text="field.text"
            :value="diagnostic[field.key]"
          />
        </div>
        <div class="my-8 mb-0">
          <QualityDiagnosticValue
            v-for="(field, idx) in familyFields"
            :key="`family-${idx}`"
            :text="field.text"
            :value="diagnostic[field.key]"
          />
        </div>
        <div v-if="isDetailedDiagnostic">
          <h6 class="font-weight-bold fr-text grey--text text--darken-3 mt-4">
            Catégories EGAlim par famille de produit
          </h6>
          <FamiliesGraph :diagnostic="diagnostic" :height="$vuetify.breakpoint.xs ? '440px' : '380px'" />
        </div>
        <v-btn
          v-if="hasActiveTeledeclaration"
          outlined
          small
          color="primary"
          class="fr-btn--tertiary px-2"
          :disabled="true"
        >
          <v-icon small class="mr-2">$check-line</v-icon>
          Données télédéclarées
        </v-btn>
        <v-btn
          v-else-if="showEditButton"
          outlined
          small
          color="primary"
          class="fr-btn--tertiary px-2 mb-6"
          :to="{
            name: 'DiagnosticTunnel',
            params: {
              canteenUrlComponent: canteenUrlComponent,
              year: diagnostic.year,
              measureId: 'qualite-des-produits',
            },
          }"
        >
          <v-icon small class="mr-2">$pencil-line</v-icon>
          Modifier mes données
        </v-btn>
      </template>
    </DsfrAccordion>
  </div>
  <div class="fr-text" v-else-if="usesCentralDiagnostic">
    <p>
      Une synthèse de données sera disponible dès que votre cuisine centrale remplit leur diagnostic.
    </p>
  </div>
  <div class="fr-text py-8" v-else>
    <p>
      Renseignez la valeur (en € HT) de vos achats alimentaires total et au moins un autre champ par label de produit
      pour voir la synthèse de vos données.
    </p>
    <v-btn
      v-if="showEditButton"
      class="mt-6"
      color="primary"
      :to="{
        name: 'DiagnosticTunnel',
        params: {
          canteenUrlComponent: canteenUrlComponent,
          year: diagnostic.year,
          measureId: 'qualite-des-produits',
        },
      }"
    >
      Compléter mes données
    </v-btn>
  </div>
</template>

<script>
import ApproGraph from "@/components/ApproGraph"
import FamiliesGraph from "@/components/FamiliesGraph"
import DsfrAccordion from "@/components/DsfrAccordion"
import QualityDiagnosticValue from "./QualityDiagnosticValue"
import { hasDiagnosticApproData, applicableDiagnosticRules, getApproPercentages } from "@/utils"

export default {
  name: "QualityMeasureSummary",
  components: { ApproGraph, FamiliesGraph, DsfrAccordion, QualityDiagnosticValue },
  props: {
    diagnostic: {},
    usesCentralDiagnostic: {},
    usesPurchasesData: {
      type: Boolean,
      required: false,
    },
    canteen: {
      type: Object,
      required: true,
    },
    showEditButton: {
      type: Boolean,
      required: false,
    },
  },
  data() {
    return {
      totalFields: [
        {
          text: "Total (en € HT) de mes achats alimentaires",
          key: "valueTotalHt",
        },
        {
          text: "Total (en € HT) de mes achats en viandes et volailles fraiches ou surgelées",
          key: "valueMeatPoultryHt",
        },
        {
          text: "Total (en € HT) de mes achats en poissons, produits de la mer et de l'aquaculture",
          key: "valueFishHt",
        },
      ],
      egalimFields: [
        {
          text: "Total (en € HT) de mes achats Bio ou en conversion Bio",
          key: "valueBioHt",
        },
        {
          text: "Total (en € HT) de mes achats SIQO (Label Rouge, AOC / AOP, IGP, STG)",
          key: "valueSustainableHt",
        },
        {
          text: "Total (en € HT) des autres achats EGAlim",
          key: "valueEgalimOthersHt",
        },
        {
          text:
            "Total (en € HT) de mes achats prenant en compte les coûts imputés aux externalités environnementales ou acquis sur la base de leurs performances en matière environnementale",
          key: "valueExternalityPerformanceHt",
        },
      ],
      familyFields: [
        {
          text: "Total (en € HT) de mes achats EGAlim en viandes et volailles fraiches ou surgelées",
          key: "valueMeatPoultryEgalimHt",
        },
        {
          text: "Total (en € HT) de mes achats provenance France en viandes et volailles fraiches ou surgelées",
          key: "valueMeatPoultryFranceHt",
        },
        {
          text: "Total (en € HT) de mes achats EGAlim en poissons, produits de la mer et de l'aquaculture",
          key: "valueFishEgalimHt",
        },
      ],
    }
  },
  computed: {
    hasApproData() {
      return hasDiagnosticApproData(this.diagnostic)
    },
    applicableRules() {
      return applicableDiagnosticRules(this.canteen, this.diagnostic.year)
    },
    percentages() {
      return getApproPercentages(this.diagnostic)
    },
    isDetailedDiagnostic() {
      return this.diagnostic.diagnosticType === "COMPLETE" || this.usesPurchasesData
    },
    hasActiveTeledeclaration() {
      return this.diagnostic?.teledeclaration?.status === "SUBMITTED"
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
  },
}
</script>

<style scoped>
hr {
  border: none;
  height: 1px;
  /* Set the hr color */
  color: #929292; /* old IE */
  background-color: #929292; /* Modern Browsers */
}
span.percentage {
  display: inline-block;
  width: 3em;
  text-align: right;
}
</style>
