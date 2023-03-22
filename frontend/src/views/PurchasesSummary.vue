<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'PurchasesHome' } }]" />
    <div>
      <h1 class="font-weight-black text-h5 text-sm-h4 mb-4" style="width: 100%">
        La synthèse de mes achats
      </h1>
      <v-row class="pb-3">
        <v-col cols="12" sm="6">
          <DsfrAutocomplete
            hide-details="auto"
            :items="userCanteens"
            placeholder="Choisissez la cantine"
            v-model="vizCanteenId"
            item-text="name"
            item-value="id"
            id="canteen"
            auto-select-first
            no-data-text="Pas de résultats"
            label="Cantine"
          />
        </v-col>
        <v-col cols="12" sm="4">
          <DsfrSelect label="Année" v-model="vizYear" :items="allowedYears" hide-details="auto" />
        </v-col>
      </v-row>
      <div v-if="displayMultiYearSummary">
        <!-- TODO: a11y -->
        <MultiYearSummaryStatistics
          :diagnostics="yearlySummary"
          height="260"
          :width="$vuetify.breakpoint.mdAndUp ? '800px' : '100%'"
          :applicableRules="applicableRules"
          :showTotal="true"
        />
      </div>
      <div v-if="summary">
        <v-row class="mb-2">
          <v-col cols="12" sm="6" md="4" v-if="summary.valueTotalHt">
            <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
              <p class="ma-0">
                <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
                  {{ toCurrency(summary.valueTotalHt) }}
                </span>
                <span class="caption">
                  total HT
                </span>
              </p>
            </v-card>
          </v-col>
          <v-col col="8" sm="6" v-if="summary.valueTotalHt && (showMealCountField || !mealCost)">
            <v-card class="fill-height text-center pa-4 d-flex flex-column justify-center" outlined>
              <v-form ref="mealCountForm" @submit.prevent>
                <label for="yearly-meals" class="body-2 d-block mb-2 text-left">
                  <span v-if="!yearlyMealCount">
                    Afin de calculer le prix par repas, veuillez renseigner le nombre total de couverts à
                  </span>
                  <span v-else>Nombre total de couverts à&nbsp;</span>
                  <b>l'année</b>
                  <span v-if="isCentralCanteen">&nbsp;(y compris les couverts livrés)</span>
                </label>
                <v-row>
                  <v-col cols="8">
                    <DsfrTextField
                      id="yearly-meals"
                      hide-details="auto"
                      :rules="[validators.greaterThanZero]"
                      v-model.number="newYearlyMealCount"
                      prepend-icon="$restaurant-fill"
                    />
                  </v-col>
                  <v-col cols="2">
                    <v-btn color="primary" @click="saveMealCount">
                      Valider
                    </v-btn>
                  </v-col>
                </v-row>
              </v-form>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6" v-else-if="mealCost">
            <v-card class="fill-height text-center py-6 d-flex flex-column justify-center" outlined>
              <p class="ma-0">
                <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
                  {{ toCurrency(mealCost) }}
                </span>
                <span class="caption">
                  coût par repas éstimé
                </span>
              </p>
              <p class="caption grey--text text--darken-2 mb-0 mt-2">
                Ce montant est obtenu en divisant le total de vos achats
                <br v-if="$vuetify.breakpoint.smAndUp" />
                par le nombre de repas par an de votre établissement ({{ yearlyMealCount }}).
              </p>
              <v-btn @click="showMealCountField = true" plain class="text-decoration-underline px-1">
                Modifier le nombre de repas par an
              </v-btn>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6" md="5" v-if="bioPercent">
            <v-card class="fill-height text-center py-6 d-flex flex-column justify-center" outlined>
              <p class="ma-0">
                <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ bioPercent }} %</span>
                <span class="caption">
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
          <v-col cols="12" sm="6" md="5" v-if="sustainablePercent">
            <v-card class="fill-height text-center py-6 d-flex flex-column justify-center" outlined>
              <p class="ma-0">
                <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ sustainablePercent }} %</span>
                <span class="caption">
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
        <FamiliesGraph :diagnostic="summary" :height="$vuetify.breakpoint.xs ? '440px' : '380px'" class="mt-4" />
      </div>
      <!-- TODO: a11y description -->
      <div v-if="loading" style="height: 250px">
        <v-progress-circular indeterminate style="left: 50%; top: 50%"></v-progress-circular>
      </div>
    </div>
  </div>
</template>

<script>
import {
  lastYear,
  diagnosticYears,
  normaliseText,
  getPercentage,
  getSustainableTotal,
  toCurrency,
  applicableDiagnosticRules,
} from "@/utils"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrSelect from "@/components/DsfrSelect"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import DsfrTextField from "@/components/DsfrTextField"
import FamiliesGraph from "@/components/FamiliesGraph"
import MultiYearSummaryStatistics from "@/components/MultiYearSummaryStatistics"
import labels from "@/data/quality-labels.json"
import validators from "@/validators"

export default {
  name: "PurchasesSummary",
  components: {
    BreadcrumbsNav,
    DsfrSelect,
    DsfrAutocomplete,
    DsfrTextField,
    FamiliesGraph,
    MultiYearSummaryStatistics,
  },
  data() {
    return {
      vizYear: lastYear(),
      vizCanteenId: null,
      vizCanteen: null,
      allowedYears: diagnosticYears().filter((year) => year <= lastYear() + 1),
      yearlySummary: null,
      summary: null,
      loading: false,
      labels,
      validators,
      newYearlyMealCount: null,
      showMealCountField: false,
    }
  },
  computed: {
    userCanteens() {
      const canteens = this.$store.state.userCanteenPreviews
      return canteens.sort((a, b) => {
        return normaliseText(a.name) > normaliseText(b.name) ? 1 : 0
      })
    },
    bioPercent() {
      return this.summary && getPercentage(this.summary.valueBioHt, this.summary.valueTotalHt)
    },
    sustainablePercent() {
      return this.summary && getPercentage(getSustainableTotal(this.summary), this.summary.valueTotalHt)
    },
    yearlyMealCount() {
      return this.vizCanteen?.yearlyMealCount
    },
    mealCost() {
      if (!this.summary || !this.yearlyMealCount) return
      return this.summary.valueTotalHt / this.yearlyMealCount
    },
    isCentralCanteen() {
      return ["central", "central_serving"].includes(this.vizCanteen?.productionType)
    },
    applicableRules() {
      return applicableDiagnosticRules(this.vizCanteen)
    },
    displayMultiYearSummary() {
      return this.yearlySummary ? Object.keys(this.yearlySummary).length > 1 : false
    },
  },
  methods: {
    getPurchaseSummaryForCanteenAndYear() {
      this.summary = null
      if (!this.vizCanteenId || !this.vizYear) return
      this.loading = true
      fetch(`/api/v1/canteenPurchasesSummary/${this.vizCanteenId}?year=${this.vizYear}`)
        .then((response) => (response.ok ? response.json() : {}))
        .then((response) => {
          this.summary = response
        })
        .finally(() => (this.loading = false))
    },
    getPurchaseSummaryForCanteen() {
      this.yearlySummary = null
      if (!this.vizCanteenId) return
      this.loading = true
      fetch(`/api/v1/canteenPurchasesSummary/${this.vizCanteenId}`)
        .then((response) => (response.ok ? response.json() : {}))
        .then((response) => {
          const results = response.results
          const yearlySummary = {}
          // reformatting for MultiYearSummaryStatistics
          results.forEach((result) => (yearlySummary[result.year] = result))
          this.yearlySummary = yearlySummary
        })
        .finally(() => (this.loading = false))
    },
    toCurrency(value) {
      return toCurrency(value)
    },
    fetchCanteen(id) {
      this.$store
        .dispatch("fetchCanteen", { id })
        .then((canteen) => {
          this.vizCanteen = canteen
          this.newYearlyMealCount = this.vizCanteen.yearlyMealCount
          this.showMealCountField = false
        })
        .catch(() => (this.vizCanteen = null))
    },
    saveMealCount() {
      if (!this.vizCanteen) return
      if (!this.$refs.mealCountForm.validate()) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }
      this.$store
        .dispatch("updateCanteen", {
          id: this.vizCanteen.id,
          payload: {
            yearlyMealCount: this.newYearlyMealCount,
          },
        })
        .then(() => this.fetchCanteen(this.vizCanteen.id))
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
  },
  watch: {
    vizCanteenId(newCanteen) {
      if (newCanteen) {
        this.getPurchaseSummaryForCanteen()
        this.getPurchaseSummaryForCanteenAndYear()
        this.vizCanteen = null
        this.fetchCanteen(newCanteen)
      }
    },
    vizYear(newYear, oldYear) {
      if (oldYear && newYear) this.getPurchaseSummaryForCanteenAndYear()
    },
  },
  mounted() {
    fetch("/api/v1/purchases/?limit=1&ordering=-date")
      .then((response) => {
        if (response.status < 200 || response.status >= 400) throw new Error()
        return response.json()
      })
      .then((response) => {
        const purchase = response.results[0]
        this.vizCanteenId = purchase.canteen
        this.vizYear = new Date(purchase.date).getFullYear()
      })
      .finally(() => {
        if (!this.vizCanteenId && this.userCanteens?.length) {
          this.vizCanteenId = this.userCanteens[0].id
        }
      })
  },
}
</script>
