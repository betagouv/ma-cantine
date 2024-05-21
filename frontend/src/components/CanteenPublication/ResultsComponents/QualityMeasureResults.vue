<template>
  <div>
    <CentralKitchenInfo :canteen="canteen" />

    <p v-if="canteen.badges.appro">
      Ce qui est servi dans les assiettes est au moins à {{ applicableRules.qualityThreshold }} % de produits durables
      et de qualité, dont {{ applicableRules.bioThreshold }} % bio, en respectant
      <a href="https://ma-cantine.agriculture.gouv.fr/blog/16">les seuils d'Outre-mer</a>
    </p>
    <p v-else>Cet établissement ne respecte pas encore la loi EGAlim pour cette mesure.</p>

    <div v-if="tabs.length" class="mb-8">
      <v-row class="align-end flex-wrap mb-4">
        <v-col>
          <DsfrSegmentedControl v-model="tab" legend="Bilan par période" :noLegend="editable" :items="tabs" />
        </v-col>
        <v-col v-if="!editable && diagnosticForYear" align="right">
          <DsfrCallout icon=" " :color="color" class="py-6 pr-14 my-0" style="width: fit-content;">
            <div class="text-left">
              <p class="mb-0">
                <b v-if="teledeclared">Données officielles</b>
                <b v-else-if="provisional">Données provisoires</b>
                <b v-else>Données non télédéclarées</b>
              </p>
            </div>
            <!-- TODO: link to article -->
          </DsfrCallout>
        </v-col>
      </v-row>
      <div v-if="tab === 'Comparer'">
        <MultiYearSummaryStatistics
          :diagnostics="graphDiagnostics"
          headingId="appro-heading"
          height="260"
          :width="$vuetify.breakpoint.mdAndUp ? '650px' : '100%'"
          :applicableRules="applicableRules"
          colorTheme="grey"
        />
      </div>
      <div v-else-if="!diagnosticForYear">
        <p>
          Données non disponibles
        </p>
      </div>
      <div v-else>
        <DsfrCallout v-if="editable" icon=" " :color="color" class="my-4 py-4 pr-14">
          <div v-if="teledeclared" class="py-4">
            <p class="mb-0">
              <b>Données officielles {{ tab }} télédéclarées</b>
              : le bilan ci-dessous a été officiellement transmis à l’administration et il est pris en compte dans le
              rapport annuel public remis au Parlement. Vos données sont publiées par défaut sur votre vitrine en ligne.
            </p>
          </div>
          <DsfrToggle
            v-else
            v-model="publishedToggleState"
            @input="updateDiagnosticPublication"
            :labelLeft="true"
            checkedLabel="Visible"
            uncheckedLabel="Caché"
          >
            <template v-slot:label>
              <span v-if="provisional" class="mb-0">
                <b>Total des achats au {{ lastPurchaseDate }}</b>
                : le bilan provisoire ci-dessous est réalisé à partir des données d’achat au {{ lastPurchaseDate }}. Vos
                données sont visibles par défaut sur votre affiche et en ligne.
              </span>
              <span v-else>
                <!-- TODO: DSFR recommends labels be <= 3 words long -->
                <b>Données non télédéclarées</b>
                : le bilan des achats de l'année {{ tab }} n'a pas été officiellement télédéclaré à l'administration. Il
                est visible par défaut sur votre affiche et en ligne, mais vous pouvez le retirer.
              </span>
            </template>
          </DsfrToggle>
        </DsfrCallout>

        <ApproGraph v-if="diagnosticForYear" :diagnostic="diagnosticForYear" :canteen="canteen" class="my-8" />

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
    </div>
    <EditableCommentsField
      :canteen="canteen"
      valueKey="qualityComments"
      :editable="editable"
      label="Commentaire"
      helpText="Si vous le souhaitez, ajoutez des précisions sur vos résultats : actions entreprises, priorités à venir..."
      cta="Modifier le commentaire"
      :charLimit="500"
      class="mb-8"
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
import DsfrCallout from "@/components/DsfrCallout"
import DsfrToggle from "@/components/DsfrToggle"

export default {
  name: "QualityMeasureResults",
  props: {
    badge: Object,
    canteen: {
      type: Object,
      required: true,
    },
    approDiagnostics: Array,
    editable: Boolean,
  },
  components: {
    CentralKitchenInfo,
    DsfrSegmentedControl,
    ApproGraph,
    EditableCommentsField,
    MultiYearSummaryStatistics,
    DsfrAccordion,
    DsfrCallout,
    DsfrToggle,
  },
  data() {
    return {
      approData: this.approDiagnostics,
      redactedYears: this.canteen.redactedApproYears || [],
      tabs: [],
      tab: undefined,
      // it is published if it is not redacted
      publishedToggleState: undefined,
      thisYear: new Date().getFullYear(),
    }
  },
  computed: {
    diagnostic() {
      if (!this.approData) return
      return latestCreatedDiagnostic(this.approData)
    },
    diagnosticForYear() {
      return this.approData.find((d) => d.year === +this.tab)
    },
    teledeclared() {
      return !!this.diagnosticForYear?.isTeledeclared
    },
    provisional() {
      return this.diagnosticForYear?.year >= this.thisYear
    },
    color() {
      // these are the same as the colours for "bio" in ApproGraph
      if (this.teledeclared) return "#21402c"
      if (this.provisional) return "#263b58"
      return "#543125"
    },
    lastPurchaseDate() {
      if (!this.provisional) return
      if (!this.diagnosticForYear) return
      const date = new Date(this.diagnosticForYear.lastPurchaseDate)
      return date.toLocaleString("fr-FR", {
        day: "numeric",
        month: "long",
        year: "numeric",
      })
    },
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
    hasPercentages() {
      return !!this.diagnosticForYear && "percentageValueTotalHt" in this.diagnosticForYear
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
      if (!this.approData || this.approData.length === 0) return null
      const diagnostics = {}
      for (let i = 0; i < this.approData.length; i++) {
        const diagnostic = this.approData[i]
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
    updateDiagnosticPublication(value) {
      if (!this.diagnosticForYear) {
        this.$store.dispatch("notifyServerError")
        return
      }
      const year = this.diagnosticForYear.year
      if (!year) {
        console.error("attempt to change redacted appro year without diagnostic year")
        return
      }
      const toRedact = value === false
      const redactedYears = [...new Set(this.redactedYears)] // get unique values just in case
      if (toRedact) {
        redactedYears.push(year)
      } else {
        const yearIdx = redactedYears.indexOf(year)
        if (yearIdx > -1) {
          redactedYears.splice(yearIdx, 1)
        }
      }
      this.$set(this, "redactedYears", redactedYears)
      const payload = {
        redactedApproYears: this.redactedYears,
      }
      return this.$store
        .dispatch("updateCanteen", {
          id: this.canteen.id,
          payload: payload,
        })
        .then(() => {
          const descriptor = toRedact ? "dépubliées" : "publiées"
          this.$store.dispatch("notify", {
            status: "success",
            message: `Les données de ${this.diagnosticForYear.year} sont bien ${descriptor}`,
          })
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
          return Promise.reject()
        })
    },
    getPublicationState(year) {
      return this.redactedYears.indexOf(year) === -1
    },
    getPurchasesSummary() {
      return fetch(`/api/v1/canteenPurchasesPercentageSummary/${this.canteen.id}?year=${this.thisYear}`)
        .then((response) => (response.ok ? response.json() : undefined))
        .then((response) => {
          if (response) {
            response.year = this.thisYear
            this.approData.push(response)
          }
        })
    },
    makeTabs() {
      const tabs = this.approData.map((d) => ({
        text: +d.year,
        value: +d.year,
        disabled: false,
      }))
      tabs.sort((a, b) => b.value - a.value)
      if (tabs.length) {
        const compareTab = {
          text: "Comparer",
          value: "Comparer",
          disabled: tabs.length < 2,
        }
        tabs.push(compareTab)
      }
      this.tabs = tabs
      this.tab = tabs[0].value
    },
  },
  mounted() {
    this.publishedToggleState = this.getPublicationState(this.tab)
    return this.getPurchasesSummary().finally(() => this.makeTabs())
  },
  watch: {
    tab(newValue) {
      const year = +newValue
      if (year !== newValue) this.publishedToggleState = this.getPublicationState(+newValue)
    },
  },
}
</script>
