<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'PurchasesHome' } }]" />
    <div>
      <h1 class="font-weight-black text-h5 text-sm-h4 mb-4" style="width: 100%">
        La synthèse de mes achats
      </h1>
      <p>
        Choisissez la cantine et l'année pour voir la répartition par label de vos achats
      </p>
      <v-row class="mb-2">
        <v-col cols="12" sm="6">
          <!-- <label cla for="canteen">Cantine</label> -->
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
      <VueApexCharts v-if="series" :options="chartOptions" :series="series" role="img" height="auto" width="100%" />
      <!-- TODO: a11y description -->
    </div>
  </div>
</template>

<script>
import { lastYear, diagnosticYears, normaliseText, capitalise } from "@/utils"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import VueApexCharts from "vue-apexcharts"
import Constants from "@/constants"
import DsfrSelect from "@/components/DsfrSelect"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"

export default {
  name: "PurchasesSummary",
  components: { BreadcrumbsNav, VueApexCharts, DsfrSelect, DsfrAutocomplete },
  data() {
    return {
      vizYear: lastYear(),
      vizData: null,
      vizCanteen: null,
      allowedYears: diagnosticYears().map((year) => {
        return {
          text: year + (year > lastYear() ? " (prévisionnel)" : ""),
          value: year,
        }
      }),
    }
  },
  computed: {
    chartOptions() {
      const legendPosition = this.$vuetify.breakpoint.smAndUp ? "right" : "top"
      const legendAlign = this.$vuetify.breakpoint.smAndUp ? "left" : "center"
      return {
        chart: {
          type: "bar",
          stacked: true,
          stackType: "100%",
          toolbar: { tools: { download: false } },
          animations: {
            enabled: false,
          },
        },
        plotOptions: {
          bar: {
            horizontal: true,
          },
        },
        states: {
          hover: {
            filter: {
              type: "darken",
              value: 0.75,
            },
          },
        },
        xaxis: {
          categories: Object.values(Constants.ProductFamilies).map((f) => this.capitalise(f.shortText)),
          title: {
            text: "Pourcentage par famille",
          },
        },
        yaxis: {
          title: {
            text: "Famille de produit",
          },
        },
        legend: {
          position: legendPosition,
          horizontalAlign: legendAlign,
        },
        dataLabels: {
          enabled: false,
        },
      }
    },
    series() {
      if (!this.vizData) return
      return this.egalimCharacteristics.map(([key, c]) => ({
        name: c.text,
        color: c.colorHex,
        data: this.vizData[key],
      }))
    },
    egalimCharacteristics() {
      return Object.entries(Constants.TeledeclarationCharacteristics).filter(([, value]) => !value.additional)
    },
    userCanteens() {
      const canteens = this.$store.state.userCanteenPreviews
      return canteens.sort((a, b) => {
        return normaliseText(a.name) > normaliseText(b.name) ? 1 : 0
      })
    },
  },
  methods: {
    capitalise: capitalise,
    camelise(str) {
      return str
        .split("_")
        .map((s) => this.capitalise(s.toLowerCase()))
        .join("")
    },
    getCharacteristicByFamilyData() {
      if (!this.vizCanteen || !this.vizYear) return
      fetch(`/api/v1/canteenPurchasesSummary/${this.vizCanteen}?year=${this.vizYear}`)
        .then((response) => (response.ok ? response.json() : {}))
        .then((response) => {
          this.vizData = {}
          this.egalimCharacteristics.forEach(([char]) => {
            this.vizData[char] = []
            Object.keys(Constants.ProductFamilies).forEach((family) => {
              const key = `value${this.camelise(family)}${this.camelise(char)}`
              this.vizData[char].push(response[key] || 0)
            })
          })
        })
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
    if (this.userCanteens && this.userCanteens.length > 0) this.vizCanteen = this.userCanteens[0].id
  },
}
</script>
