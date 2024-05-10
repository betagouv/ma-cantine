<template>
  <div class="mb-8">
    <CentralKitchenInfo :canteen="canteen" />

    <p v-if="badge.earned">
      Ce qui est servi dans les assiettes est au moins à {{ applicableRules.qualityThreshold }} % de produits durables
      et de qualité, dont {{ applicableRules.bioThreshold }} % bio, en respectant
      <a href="https://ma-cantine.agriculture.gouv.fr/blog/16">les seuils d'Outre-mer</a>
    </p>
    <p v-else>Cet établissement ne respecte pas encore la loi EGAlim pour cette mesure.</p>

    <DsfrSegmentedControl v-model="tab" legend="Année" noLegend :items="tabs" />
    <div v-if="diagnosticForYear">
      <ApproGraph v-if="diagnosticForYear" :diagnostic="diagnosticForYear" :canteen="canteen" />

      <div v-if="hasFamilyDetail">
        <DsfrAccordion :items="[{ title: 'Détail par famille de produit' }]" class="mb-2">
          <template v-slot:content>
            <v-row class="text-center pt-3 pb-2">
              <v-col cols="12" sm="4" class="pa-4">
                <v-icon large class="grey--text text--darken-3 mb-2">$award-line</v-icon>
                <p class="mb-0">
                  <span class="font-weight-bold percentage">{{ meatEgalimPercentage || "—" }} %</span>
                  de viandes et volailles
                  <br />
                  EGAlim
                </p>
              </v-col>
              <v-col cols="12" sm="4" class="pa-4">
                <v-icon large class="grey--text text--darken-3 mb-2">$france-line</v-icon>
                <p class="mb-0">
                  <span class="font-weight-bold percentage">{{ meatFrancePercentage || "—" }} %</span>
                  de viandes et volailles
                  <br />
                  provenance France
                </p>
              </v-col>
              <v-col cols="12" sm="4" class="pa-4">
                <v-icon large class="grey--text text--darken-3 mb-2">$anchor-line</v-icon>
                <p class="mb-0">
                  <span class="font-weight-bold percentage">{{ fishEgalimPercentage || "—" }} %</span>
                  de produits de la mer
                  <br />
                  et aquaculture EGAlim
                </p>
              </v-col>
            </v-row>
          </template>
        </DsfrAccordion>
      </div>
    </div>
    <div v-else>
      <MultiYearSummaryStatistics
        :diagnostics="graphDiagnostics"
        headingId="appro-heading"
        height="260"
        :width="$vuetify.breakpoint.mdAndUp ? '650px' : '100%'"
        :applicableRules="applicableRules"
      />
    </div>
    <EditableCommentsField
      :canteen="canteen"
      valueKey="qualityComments"
      :editable="editable"
      label="Commentaire"
      helpText="Si vous le souhaitez, ajoutez des précisions sur vos résultats : actions entreprises, priorités à venir..."
      cta="Modifier le commentaire"
      :charLimit="500"
    />
  </div>
</template>

<script>
import { applicableDiagnosticRules, getPercentage, latestCreatedDiagnostic } from "@/utils"
import CentralKitchenInfo from "./CentralKitchenInfo"
import DsfrSegmentedControl from "@/components/DsfrSegmentedControl"
import ApproGraph from "@/components/ApproGraph"
import EditableCommentsField from "../EditableCommentsField"
import MultiYearSummaryStatistics from "@/components/MultiYearSummaryStatistics"
import DsfrAccordion from "@/components/DsfrAccordion"

const COMPARE_TAB = "Comparer"

export default {
  name: "QualityMeasureResults",
  props: {
    badge: Object,
    canteen: Object,
    diagnosticSet: Array,
    editable: Boolean,
  },
  components: {
    CentralKitchenInfo,
    DsfrSegmentedControl,
    ApproGraph,
    EditableCommentsField,
    MultiYearSummaryStatistics,
    DsfrAccordion,
  },
  data() {
    const tabs = this.diagnosticSet.map((d) => +d.year)
    tabs.sort((a, b) => b - a)
    tabs.push(COMPARE_TAB)
    return {
      tabs,
      tab: tabs[0],
    }
  },
  computed: {
    diagnostic() {
      if (!this.diagnosticSet) return
      return latestCreatedDiagnostic(this.diagnosticSet)
    },
    diagnosticForYear() {
      return this.diagnosticSet.find((d) => d.year === +this.tab)
    },
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
    hasPercentages() {
      return "percentageValueTotalHt" in this.diagnosticForYear
    },
    meatEgalimPercentage() {
      return this.hasPercentages
        ? this.toPercentage(this.diagnosticForYear.percentageValueMeatPoultryEgalimHt)
        : getPercentage(this.diagnosticForYear.valueMeatPoultryEgalimHt, this.diagnosticForYear.valueMeatPoultryHt)
    },
    meatFrancePercentage() {
      return this.hasPercentages
        ? this.toPercentage(this.diagnosticForYear.percentageValueMeatPoultryFranceHt)
        : getPercentage(this.diagnosticForYear.valueMeatPoultryFranceHt, this.diagnosticForYear.valueMeatPoultryHt)
    },
    fishEgalimPercentage() {
      return this.hasPercentages
        ? this.toPercentage(this.diagnosticForYear.percentageValueFishEgalimHt)
        : getPercentage(this.diagnosticForYear.valueFishEgalimHt, this.diagnosticForYear.valueFishHt)
    },
    graphDiagnostics() {
      if (!this.diagnosticSet || this.diagnosticSet.length === 0) return null
      const diagnostics = {}
      for (let i = 0; i < this.diagnosticSet.length; i++) {
        const diagnostic = this.diagnosticSet[i]
        diagnostics[diagnostic.year] = diagnostic
      }
      return diagnostics
    },
    hasFamilyDetail() {
      return this.meatEgalimPercentage || this.meatFrancePercentage || this.fishEgalimPercentage
    },
  },
  methods: {
    toPercentage(value) {
      return Math.round(value * 100)
    },
  },
}
</script>
