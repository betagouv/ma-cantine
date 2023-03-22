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
import { getPercentage, hasDiagnosticApproData, getSustainableTotal } from "@/utils"

const VALUE_DESCRIPTION = "Pourcentage d'achats"
const BIO = "Bio"
const SUSTAINABLE = "Qualité et durable (hors bio)"
const OTHER = "Hors EGAlim"
const TOTAL = "Total HT"

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
    showTotal: Boolean,
  },
  data() {
    let years = []
    const diagArray = Object.values(this.diagnostics)
    const completedDiagnostics = []
    const thisYear = new Date().getFullYear()
    diagArray.forEach((d) => {
      if (hasDiagnosticApproData(d)) {
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
        // TODO: review these with complete diags in mind
        bio: this.completedDiagnostics.map((d) => getPercentage(d.valueBioHt, d.valueTotalHt) || 0),
        sustainable: this.completedDiagnostics.map((d) => getPercentage(getSustainableTotal(d), d.valueTotalHt) || 0),
        other: this.completedDiagnostics.map((d) => {
          return (
            100 -
            (getPercentage(d.valueBioHt, d.valueTotalHt) || 0) -
            getPercentage(getSustainableTotal(d), d.valueTotalHt || 0)
          )
        }),
        total: this.completedDiagnostics.map((d) => d.valueTotalHt),
      }
    },
    series() {
      const data = [
        {
          name: BIO,
          data: this.seriesData.bio,
          type: "column",
          color: "#297254",
        },
        {
          name: SUSTAINABLE,
          data: this.seriesData.sustainable,
          type: "column",
          color: "#00A95F",
          foreColor: "#000",
        },
        {
          name: OTHER,
          data: this.seriesData.other,
          type: "column",
          color: "#ccc",
        },
      ]
      if (this.showTotal) {
        data.push({
          name: TOTAL,
          data: this.seriesData.total,
          type: "line",
          color: "#000091",
        })
      }
      return data
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
      const yaxis = [
        {
          seriesName: BIO,
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
        {
          seriesName: SUSTAINABLE,
          labels: {
            formatter: percentageFormatter,
          },
          show: false,
        },
        {
          seriesName: OTHER,
          labels: {
            formatter: percentageFormatter,
          },
          show: false,
        },
      ]
      if (this.showTotal) {
        yaxis.push({
          seriesName: TOTAL,
          opposite: true,
          title: {
            text: this.$vuetify.breakpoint.xs ? undefined : "Somme d'achats",
          },
          labels: {
            formatter: currencyFormatter,
          },
        })
      }

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
        yaxis,
        stroke: {
          width: [0, 0, 0, 2],
          curve: "straight",
        },
        markers: {
          size: 3,
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
  },
}

function percentageFormatter(val) {
  return val + " %"
}

function currencyFormatter(val) {
  return val + " €"
}
</script>

<style scoped>
div >>> .apexcharts-legend.apexcharts-align-left {
  text-align: left;
}
</style>
