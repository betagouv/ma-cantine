<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'PurchasesHome' } }]" />
    <div>
      <h1 class="font-weight-black text-h5 text-sm-h4 mb-4" style="width: 100%">
        La synthèse de mes achats
      </h1>
      <v-row class="mb-2">
        <v-col cols="12" sm="6">
          <DsfrAutocomplete
            hide-details="auto"
            :items="userCanteens"
            placeholder="Choisissez la cantine"
            v-model="vizCanteen"
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
      <v-row v-if="summary">
        <v-col cols="12" sm="6" md="4" v-if="summary.valueTotalHt">
          <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
            <p class="ma-0">
              <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
                {{ toCurrency(summary.valueTotalHt) }}
              </span>
              <span class="caption grey--text text--darken-2">
                total HT
              </span>
            </p>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="4" v-if="summary.valueBioHt">
          <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
            <p class="ma-0">
              <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ bioPercent }} %</span>
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
        <v-col cols="12" sm="6" md="4" v-if="summary.valueSustainableHt">
          <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
            <p class="ma-0">
              <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ sustainablePercent }} %</span>
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
      <FamiliesGraph
        v-if="summary"
        :diagnostic="summary"
        :height="$vuetify.breakpoint.xs ? '440px' : '380px'"
        class="mt-4"
      />
      <!-- TODO: a11y description -->
      <div v-if="loading" style="height: 250px">
        <v-progress-circular indeterminate style="left: 50%; top: 50%"></v-progress-circular>
      </div>
    </div>
  </div>
</template>

<script>
import { lastYear, diagnosticYears, normaliseText, getPercentage, getSustainableTotal, toCurrency } from "@/utils"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrSelect from "@/components/DsfrSelect"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import FamiliesGraph from "@/components/FamiliesGraph"
import labels from "@/data/quality-labels.json"

export default {
  name: "PurchasesSummary",
  components: { BreadcrumbsNav, DsfrSelect, DsfrAutocomplete, FamiliesGraph },
  data() {
    return {
      vizYear: lastYear(),
      vizCanteen: null,
      allowedYears: diagnosticYears().filter((year) => year <= lastYear() + 1),
      summary: null,
      loading: false,
      labels,
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
  },
  methods: {
    getCharacteristicByFamilyData() {
      this.summary = null
      if (!this.vizCanteen || !this.vizYear) return
      this.loading = true
      fetch(`/api/v1/canteenPurchasesSummary/${this.vizCanteen}?year=${this.vizYear}`)
        .then((response) => (response.ok ? response.json() : {}))
        .then((response) => {
          this.summary = response
        })
        .finally(() => (this.loading = false))
    },
    toCurrency(value) {
      return toCurrency(value)
    },
  },
  watch: {
    vizCanteen(newCanteen) {
      if (newCanteen) this.getCharacteristicByFamilyData()
    },
    vizYear(newYear, oldYear) {
      if (oldYear && newYear) this.getCharacteristicByFamilyData()
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
        this.vizCanteen = purchase.canteen
        this.vizYear = new Date(purchase.date).getFullYear()
      })
      .finally(() => {
        if (!this.vizCanteen && this.userCanteens?.length) {
          this.vizCanteen = this.userCanteens[0].id
        }
      })
  },
}
</script>
