<template>
  <div>
    <div v-if="years.length">
      <VueApexCharts
        :options="chartOptions"
        :series="series"
        role="img"
        :aria-labelledby="headingId"
        aria-describedby="multi-year-graph-description"
        v-if="years.length"
        :height="height || 'auto'"
        :width="width || '100%'"
      />
      <DsfrAccordion :items="[{ title: 'Description du graphique' }]" :style="`width: ${width}`" class="mb-2">
        <template v-slot:content>
          <div id="multi-year-graph-description">
            <p>
              Les pourcentages d'achats par année pour cette cantine sont :
            </p>
            <ol class="mb-4">
              <li v-for="(year, idx) in years" :key="year">
                {{ year }} : {{ seriesData.bio[idx] }} % bio, {{ seriesData.sustainable[idx] }} % de qualité et durable
                (hors bio), {{ 100 - seriesData.bio[idx] - seriesData.sustainable[idx] }} % hors EGalim
              </li>
            </ol>
            <p class="mb-0">
              Rappel de l'objectif : Les repas servis comportent au moins {{ applicableRules.qualityThreshold }} % de
              produits de qualité et durables dont au moins {{ applicableRules.bioThreshold }} % issus de l'agriculture
              biologique ou en conversion, pour les cantines
              {{
                applicableRules.hasQualityException
                  ? `dans la région « ${regionDisplayName} »`
                  : "en France métropolitaine"
              }}.
            </p>
          </div>
        </template>
      </DsfrAccordion>
    </div>
    <p v-else class="my-4 text-left">Données non renseignées</p>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts"
import DsfrAccordion from "@/components/DsfrAccordion"
import { getPercentage, getSustainableTotal, regionDisplayName } from "@/utils"

const VALUE_DESCRIPTION = "Pourcentage d'achats"
const BIO = "Bio"
const SUSTAINABLE = "Qualité et durable (hors bio)"

export default {
  components: {
    VueApexCharts,
    DsfrAccordion,
  },
  props: {
    diagnostics: Object,
    headingId: String,
    height: String,
    width: String,
    applicableRules: Object,
    legendPosition: String,
    colorTheme: {
      type: String,
      default: "green",
    },
  },
  data() {
    let years = []
    const diagArray = Object.values(this.diagnostics)
    const completedDiagnostics = []
    const thisYear = new Date().getFullYear()
    diagArray.forEach((d) => {
      completedDiagnostics.push(d)
      years.push(`${d.year}${d.year >= thisYear ? " (provisionnel)" : ""}`)
    })
    return {
      years: years.reverse(),
      completedDiagnostics: completedDiagnostics.reverse(),
    }
  },
  computed: {
    seriesData() {
      return {
        bio: this.completedDiagnostics.map(this.bioPercentage),
        sustainable: this.completedDiagnostics.map(this.sustainablePercentage),
        other: this.completedDiagnostics.map(this.otherPercentage),
        total: this.completedDiagnostics.map((d) => d.valueTotale),
      }
    },
    series() {
      return [
        {
          name: BIO,
          data: this.seriesData.bio,
          color: this.theme.bio,
        },
        {
          name: SUSTAINABLE,
          data: this.seriesData.sustainable,
          color: this.theme.sustainable,
          foreColor: "#000",
        },
      ]
    },
    chartOptions() {
      const legendPosition = this.legendPosition || (this.$vuetify.breakpoint.smAndUp ? "right" : "top")
      const legendAlign = legendPosition === "right" ? "left" : "center"
      return {
        chart: {
          type: "bar",
          stacked: true,
          toolbar: { tools: { download: false } },
          animations: {
            enabled: false,
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
          categories: this.years,
        },
        yaxis: {
          title: {
            text: this.$vuetify.breakpoint.xs ? undefined : VALUE_DESCRIPTION,
          },
          labels: {
            formatter: percentageFormatter,
          },
          max: 100,
          min: 0,
          tickAmount: 4,
        },
        annotations: {
          yaxis: [
            {
              y: this.applicableRules.qualityThreshold,
              borderColor: "#333",
            },
            {
              y: this.applicableRules.bioThreshold,
              borderColor: "#333",
            },
          ],
        },
        legend: {
          position: legendPosition,
          horizontalAlign: legendAlign,
        },
        dataLabels: {
          enabled: false,
        },
        tooltip: {
          intersect: false,
          shared: true,
        },
      }
    },
    regionDisplayName() {
      return regionDisplayName(this.applicableRules.regionForQualityException)
    },
    theme() {
      const themes = {
        green: {
          bio: "#21402c",
          sustainable: "#00A95F",
        },
        grey: {
          bio: "#3a3a3a", // grey-200
          sustainable: "#919191",
        },
      }
      return themes[this.colorTheme]
    },
  },
  methods: {
    bioPercentage(diag) {
      return "percentageValueBio" in diag
        ? Math.round(diag.percentageValueBio * 100)
        : getPercentage(diag.valueBio, diag.valueTotale)
    },
    sustainablePercentage(diag) {
      return "percentageValueTotale" in diag
        ? Math.round(getSustainableTotal(diag) * 100)
        : getPercentage(getSustainableTotal(diag), diag.valueTotale)
    },
    otherPercentage(diag) {
      return 100 - this.bioPercentage(diag) - this.sustainablePercentage(diag)
    },
  },
}

function percentageFormatter(val) {
  return val + " %"
}
</script>

<style scoped>
div >>> .apexcharts-legend.apexcharts-align-left {
  text-align: left;
}
</style>
