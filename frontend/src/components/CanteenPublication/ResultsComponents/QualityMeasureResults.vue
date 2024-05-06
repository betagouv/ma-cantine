<template>
  <div class="mb-8">
    <!-- TODO: consider where this message should be appearing. If ALL above accordions and if APPRO here? -->
    <!-- do we need to think about the case where the declaration method may change year on year ? -->
    <CentralKitchenInfo :canteen="canteen" />

    <!-- TODO: check if this text is desired -->
    <p v-if="badge.earned" class="mb-0">
      Ce qui est servi dans les assiettes est au moins à {{ applicableRules.qualityThreshold }} % de produits durables
      et de qualité, dont {{ applicableRules.bioThreshold }} % bio, en respectant
      <a href="https://ma-cantine.agriculture.gouv.fr/blog/16">les seuils d'Outre-mer</a>
    </p>
    <p v-else>Cet établissement ne respecte pas encore la loi EGAlim pour cette mesure.</p>

    <DsfrSegmentedControl v-model="tab" legend="Année" noLegend :items="tabs" />
    <div v-if="diagnosticForYear">
      <!-- callouts for each tab to explain whats up -->
      <!-- Later: option to unpublish per-year if not TD and provisional purchases -->
      <!-- colour config option: blue/green/brown -->
      <ApproGraph v-if="diagnosticForYear" :diagnostic="diagnosticForYear" :canteen="canteen" />
      <!-- provisional purchases graph (what publishing rules do we want on that?) -->
      <!-- Per-family accordion detail -->
    </div>
    <div v-else>
      <!-- TODO: multi year comparison -->
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

    <!-- <div v-if="showPercentagesBlock">
      <h2 class="font-weight-black text-h6 grey--text text--darken-4 my-4">
        Que mange-t-on dans les assiettes en {{ publicationYear }} ?
      </h2>


      <h3
        class="font-weight-black text-body-1 grey--text text--darken-4 my-4"
        v-if="
          diagnostic.diagnosticType === 'COMPLETE' ||
            meatEgalimPercentage ||
            meatFrancePercentage ||
            fishEgalimPercentage
        "
      >
        Total
      </h3>
      <v-row>
        <v-col cols="12" sm="6" md="4" v-if="bioPercentage">
          <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
            <p class="ma-0">
              <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ bioPercentage }} %</span>
              <span class="caption grey--text text--darken-2">
                bio
              </span>
            </p>
            <div class="mt-2">
              <v-img
                contain
                src="/static/images/quality-labels/logo_bio_eurofeuille.png"
                alt="Logo Agriculture Biologique"
                title="Logo Agriculture Biologique"
                max-height="35"
              />
            </div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="4" v-if="sustainablePercentage">
          <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
            <p class="ma-0">
              <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
                {{ sustainablePercentage }} %
              </span>
              <span class="caption grey--text text--darken-2">
                durables et de qualité (hors bio)
              </span>
            </p>
            <div class="d-flex mt-2 justify-center flex-wrap">
              <v-img
                contain
                v-for="label in labels"
                :key="label.title"
                :src="`/static/images/quality-labels/${label.src}`"
                :alt="label.title"
                :title="label.title"
                class="px-1"
                max-height="40"
                max-width="40"
              />
            </div>
          </v-card>
        </v-col>
      </v-row>
      <div v-if="diagnostic.diagnosticType === 'COMPLETE'">
        <h3 class="font-weight-black text-body-1 grey--text text--darken-4 mt-4">
          Catégories EGAlim par famille de produit
        </h3>
        <FamiliesGraph :diagnostic="diagnostic" :height="$vuetify.breakpoint.xs ? '440px' : '380px'" />
      </div>
      <div v-else-if="meatEgalimPercentage || meatFrancePercentage || fishEgalimPercentage">
        <h3 class="font-weight-black text-body-1 grey--text text--darken-4 mb-4 mt-8">
          Par famille de produit
        </h3>
        <v-row>
          <v-col cols="12" sm="4" md="4" v-if="meatEgalimPercentage">
            <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
              <p class="ma-0">
                <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
                  {{ meatEgalimPercentage }} %
                </span>
                <span class="caption grey--text text--darken-2">
                  viandes et volailles EGAlim
                </span>
              </p>
              <div class="mt-2">
                <v-icon size="30" color="brown">
                  mdi-food-steak
                </v-icon>
                <v-icon size="30" color="brown">
                  mdi-food-drumstick
                </v-icon>
                <v-icon size="30" color="green">
                  $checkbox-circle-fill
                </v-icon>
              </div>
            </v-card>
          </v-col>
          <v-col cols="12" sm="4" md="4" v-if="meatFrancePercentage">
            <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
              <p class="ma-0">
                <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
                  {{ meatFrancePercentage }} %
                </span>
                <span class="caption grey--text text--darken-2">
                  viandes et volailles provenance France
                </span>
              </p>
              <div class="mt-2">
                <v-icon size="30" color="brown">
                  mdi-food-steak
                </v-icon>
                <v-icon size="30" color="brown">
                  mdi-food-drumstick
                </v-icon>
                <v-icon size="30" color="indigo">
                  $france-line
                </v-icon>
              </div>
            </v-card>
          </v-col>
          <v-col cols="12" sm="4" md="4" v-if="fishEgalimPercentage">
            <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
              <p class="ma-0">
                <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
                  {{ fishEgalimPercentage }} %
                </span>
                <span class="caption grey--text text--darken-2">
                  produits aquatiques EGAlim
                </span>
              </p>
              <div class="mt-2">
                <v-icon size="30" color="blue">
                  mdi-fish
                </v-icon>
                <v-icon size="30" color="green">
                  $checkbox-circle-fill
                </v-icon>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </div>

    <div v-if="shouldDisplayGraph">
      <h2 id="appro-heading" class="font-weight-black text-h6 grey--text text--darken-4 mt-12 mb-2">
        Évolution des produits dans nos assiettes sur les années
      </h2>
      <div>
        <MultiYearSummaryStatistics
          :diagnostics="graphDiagnostics"
          headingId="appro-heading"
          height="260"
          :width="$vuetify.breakpoint.mdAndUp ? '650px' : '100%'"
          :applicableRules="applicableRules"
        />
      </div>
    </div> -->
  </div>
</template>

<script>
import {
  lastYear,
  hasDiagnosticApproData,
  applicableDiagnosticRules,
  getSustainableTotal,
  getPercentage,
  latestCreatedDiagnostic,
} from "@/utils"
import labels from "@/data/quality-labels.json"
import CentralKitchenInfo from "./CentralKitchenInfo"
import DsfrSegmentedControl from "@/components/DsfrSegmentedControl"
import ApproGraph from "@/components/ApproGraph"
import EditableCommentsField from "../EditableCommentsField"

const COMPARE_TAB = "Comparer"

export default {
  name: "QualityMeasureResults",
  props: {
    badge: Object,
    canteen: Object,
    diagnosticSet: Array,
    editable: Boolean,
  },
  components: { CentralKitchenInfo, DsfrSegmentedControl, ApproGraph, EditableCommentsField },
  data() {
    const tabs = this.diagnosticSet.map((d) => +d.year)
    tabs.sort((a, b) => b - a)
    tabs.push(COMPARE_TAB)
    return {
      labels,
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
    publicationYear() {
      return this.diagnostic?.year
    },
    showPercentagesBlock() {
      return (
        this.diagnostic &&
        (this.bioPercentage ||
          this.sustainablePercentage ||
          this.meatEgalimPercentage ||
          this.meatFrancePercentage ||
          this.fishEgalimPercentage)
      )
    },
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
    hasPercentages() {
      return "percentageValueTotalHt" in this.diagnostic
    },
    bioPercentage() {
      return this.hasPercentages
        ? this.toPercentage(this.diagnostic.percentageValueBioHt)
        : getPercentage(this.diagnostic.valueBioHt, this.diagnostic.valueTotalHt)
    },
    sustainablePercentage() {
      return this.hasPercentages
        ? this.toPercentage(getSustainableTotal(this.diagnostic))
        : getPercentage(getSustainableTotal(this.diagnostic), this.diagnostic.valueTotalHt)
    },
    meatEgalimPercentage() {
      return this.hasPercentages
        ? this.toPercentage(this.diagnostic.percentageValueMeatPoultryEgalimHt)
        : getPercentage(this.diagnostic.valueMeatPoultryEgalimHt, this.diagnostic.valueMeatPoultryHt)
    },
    meatFrancePercentage() {
      return this.hasPercentages
        ? this.toPercentage(this.diagnostic.percentageValueMeatPoultryFranceHt)
        : getPercentage(this.diagnostic.valueMeatPoultryFranceHt, this.diagnostic.valueMeatPoultryHt)
    },
    fishEgalimPercentage() {
      return this.hasPercentages
        ? this.toPercentage(this.diagnostic.percentageValueFishEgalimHt)
        : getPercentage(this.diagnostic.valueFishEgalimHt, this.diagnostic.valueFishHt)
    },
    shouldDisplayGraph() {
      if (!this.diagnosticSet || this.diagnosticSet.length === 0) return false
      const completedDiagnostics = this.diagnosticSet.filter(hasDiagnosticApproData)
      if (completedDiagnostics.length === 0) return false
      else if (completedDiagnostics.length === 1) return completedDiagnostics[0].year !== lastYear()
      else return true
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
  },
  methods: {
    toPercentage(value) {
      return Math.round(value * 100)
    },
  },
}
</script>
