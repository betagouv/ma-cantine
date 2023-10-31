<template>
  <div class="fr-text" v-if="hasApproData">
    <ApproGraph :diagnostic="displayDiagnostic" :canteen="canteen" />
    <v-row>
      <v-col cols="12" md="6">
        <h5 class="mb-4 font-weight-bold fr-text">Détail du calcul de mes taux EGAlim</h5>
        <v-row>
          <v-col cols="6">
            <p class="mb-0">Produits bio</p>
          </v-col>
          <v-col cols="2">
            <p class="mb-0 font-weight-bold color-bio">{{ percentages.bio || "—" }} %</p>
          </v-col>
          <v-col cols="4">
            <p class="mb-0 color-bio">
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
            <p class="mb-0 font-weight-bold color-egalim">{{ percentages.egalim || "—" }} %</p>
          </v-col>
          <v-col cols="4">
            <p class="mb-0 color-egalim">
              <i>objectif : {{ applicableRules.qualityThreshold }} %</i>
            </p>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="12" md="6">
        <h5 class="mb-4 font-weight-bold fr-text">Par famille de produits</h5>
        <p class="mb-md-4">
          <v-icon class="mr-2" color="#00A95F">$award-line</v-icon>
          <span class="font-weight-bold percentage">{{ percentages.meatPoultryEgalim || "—" }} %</span>
          de viandes et volailles EGAlim
        </p>
        <p class="mb-md-4">
          <v-icon class="mr-2" color="#00A95F">$france-line</v-icon>
          <span class="font-weight-bold percentage">{{ percentages.meatPoultryFrance || "—" }} %</span>
          de viandes et volailles provenance France
        </p>
        <p class="mb-md-4">
          <v-icon class="mr-2" color="#00A95F">$anchor-line</v-icon>
          <span class="font-weight-bold percentage">{{ percentages.fishEgalim || "—" }} %</span>
          de produits aquatiques EGAlim
        </p>
      </v-col>
    </v-row>
    <v-expansion-panels v-if="!usesCentralDiagnostic" hover accordion tile flat class="mt-10">
      <v-expansion-panel class="dsfr">
        <v-expansion-panel-header class="px-3 primary--text">
          <h5 class="fr-text font-weight-normal">
            Données détaillées
          </h5>
        </v-expansion-panel-header>
        <v-expansion-panel-content class="ml-n3 py-4">
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
          <div class="my-8">
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
            outlined
            small
            color="primary"
            class="fr-btn--tertiary px-2 mb-6"
            :to="{
              name: 'DiagnosticModification',
              params: {
                canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(this.canteen),
                year: diagnostic.year,
              },
            }"
          >
            <v-icon small class="mr-2">$pencil-line</v-icon>
            Modifier mes données
          </v-btn>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
  <div class="fr-text" v-else-if="usesCentralDiagnostic">
    <p>
      Une synthèse de données sera disponible dès que votre cuisine centrale remplit leur diagnostic.
    </p>
  </div>
  <div class="fr-text" v-else>
    <p>
      Renseignez la valeur (en HT) de vos achats alimentaires total et au moins un autre champ par label de produit pour
      voir la synthèse de vos données.
    </p>
    <v-btn
      color="primary"
      :to="{
        name: 'DiagnosticModification',
        params: {
          canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(this.canteen),
          year: diagnostic.year,
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
import QualityDiagnosticValue from "./QualityDiagnosticValue"
import { hasDiagnosticApproData, applicableDiagnosticRules, getApproPercentages } from "@/utils"

export default {
  name: "QualityMeasureSummary",
  components: { ApproGraph, FamiliesGraph, QualityDiagnosticValue },
  props: {
    diagnostic: {},
    centralDiagnostic: {},
    canteen: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      totalFields: [
        {
          text: "Total (en HT) de mes achats alimentaires",
          key: "valueTotalHt",
        },
        {
          text: "Total (en HT) des mes achats en viandes et volailles fraiches ou surgelées",
          key: "valueMeatPoultryHt",
        },
        {
          text: "Total (en HT) des mes achats en poissons, produits de la mer et de l'aquaculture",
          key: "valueFishHt",
        },
      ],
      egalimFields: [
        {
          text: "Total (en HT) de mes achats Bio ou en conversion Bio",
          key: "valueBioHt",
        },
        {
          text: "Total (en HT) de mes achats SIQO (AOP/AOC, IGP, STG, Label Rouge)",
          key: "valueSustainableHt",
        },
        {
          text: "Total (en HT) des autres achats EGAlim",
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
          text: "Total (en HT) des mes achats EGAlim en viandes et volailles fraiches ou surgelées",
          key: "valueMeatPoultryEgalimHt",
        },
        {
          text: "Total (en HT) des mes achats provenance France en viandes et volailles fraiches ou surgelées",
          key: "valueMeatPoultryFranceHt",
        },
        {
          text: "Total (en HT) des mes achats EGAlim en poissons, produits de la mer et de l'aquaculture",
          key: "valueFishEgalimHt",
        },
      ],
    }
  },
  computed: {
    usesCentralDiagnostic() {
      return !!this.centralDiagnostic
    },
    displayDiagnostic() {
      return this.usesCentralDiagnostic ? this.centralDiagnostic : this.diagnostic
    },
    hasApproData() {
      return hasDiagnosticApproData(this.displayDiagnostic)
    },
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
    percentages() {
      return getApproPercentages(this.displayDiagnostic)
    },
    isDetailedDiagnostic() {
      return this.diagnostic.diagnosticType === "COMPLETE"
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
.dsfr.v-expansion-panel {
  box-shadow: inset 0 1px 0 0 #ddd, 0 1px 0 0 #ddd;
}
.color-bio {
  color: #297254;
}
.color-egalim {
  color: #00a95f;
}
</style>
