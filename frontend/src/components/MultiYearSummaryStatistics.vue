<template>
  <div>
    <div v-if="years.length">
      <VueApexCharts
        :options="chartOptions"
        :series="series"
        role="img"
        :aria-labelledby="headingId"
        aria-describedby="text"
        v-if="years.length"
        :height="this.height || 'auto'"
        :width="this.width || '100%'"
      />
      <p id="text" class="d-none">{{ description }}</p>
    </div>
    <p v-else class="my-4 text-left">Données non renseignées</p>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts"
import { getPercentage, isDiagnosticApproComplete, getSustainableTotal } from "@/utils"

const VALUE_DESCRIPTION = "Pourcentage d'achats"
const BIO = "Bio"
const SUSTAINABLE = "Qualité et durable (hors bio)"
const OTHER = "Hors EGAlim"

export default {
  components: {
    VueApexCharts,
  },
  props: {
    diagnostics: Object,
    headingId: String,
    height: String,
    width: String,
    applicableRules: Object,
  },
  data() {
    let years = []
    const diagArray = Object.values(this.diagnostics)
    const completedDiagnostics = []
    const thisYear = new Date().getFullYear()
    diagArray.forEach((d) => {
      if (isDiagnosticApproComplete(d)) {
        completedDiagnostics.push(d)
        years.push(`${d.year}${d.year >= thisYear ? " (objectif)" : ""}`)
      }
    })
    return {
      years,
      completedDiagnostics,
    }
  },
  computed: {
    seriesData() {
      return {
        bio: this.completedDiagnostics.map((d) => getPercentage(d.valueBioHt, d.valueTotalHt)),
        sustainable: this.completedDiagnostics.map((d) => getPercentage(getSustainableTotal(d), d.valueTotalHt)),
        other: this.completedDiagnostics.map((d) => {
          return 100 - getPercentage(d.valueBioHt, d.valueTotalHt) - getPercentage(d.valueSustainableHt, d.valueTotalHt)
        }),
      }
    },
    series() {
      return [
        {
          name: BIO,
          data: this.seriesData.bio,
          color: "#06622f",
        },
        {
          name: SUSTAINABLE,
          data: this.seriesData.sustainable,
          color: "#55a57e",
          foreColor: "#000",
        },
        {
          name: OTHER,
          data: this.seriesData.other,
          color: "#ccc",
        },
      ]
    },
    description() {
      let description = `${VALUE_DESCRIPTION}. `
      this.years.forEach((year, idx) => {
        description += `${year} : `
        description += `${percentageFormatter(this.seriesData.bio[idx])} ${BIO}, ${percentageFormatter(
          this.seriesData.sustainable[idx]
        )} ${SUSTAINABLE}. `
      })
      return description
    },
    chartOptions() {
      const legendPosition = this.$vuetify.breakpoint.smAndUp ? "right" : "top"
      const legendAlign = this.$vuetify.breakpoint.smAndUp ? "left" : "center"
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
      }
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
