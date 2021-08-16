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
      />
      <p id="text" class="d-none">{{ description }}</p>
    </div>
    <p v-else class="my-4">Données non renseignées</p>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts"

const VALUE_DESCRIPTION = "Pourcentage du total d'achats alimentaires (en HT)"
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
  },
  data() {
    let years = []
    const diagArray = Object.values(this.diagnostics)
    const completedDiagnostics = []
    diagArray.forEach((d) => {
      if (!strictIsNaN(d.valueBioHt) && !strictIsNaN(d.valueSustainableHt) && !strictIsNaN(d.valueTotalHt)) {
        completedDiagnostics.push(d)
        years.push(d.year)
      }
    })
    return {
      years,
      completedDiagnostics,
      chartOptions: {
        chart: {
          type: "bar",
          stacked: true,
          toolbar: { tools: { download: false } },
        },
        plotOptions: {
          bar: {
            columnWidth: years.length < 3 ? "50%" : "70%",
          },
        },
        xaxis: {
          categories: years,
          title: {
            text: "Année",
          },
        },
        yaxis: {
          title: {
            text: VALUE_DESCRIPTION,
          },
          labels: {
            formatter: percentageFormatter,
          },
          max: 100,
          min: 0,
        },
        annotations: {
          yaxis: [
            {
              y: 50,
              borderColor: "#333",
              label: {
                borderColor: "#333",
                style: {
                  color: "#fff",
                  background: "#333",
                },
                text: "Objectif EGAlim 2022",
              },
            },
          ],
        },
        tooltip: {
          x: {
            formatter: percentageFormatter,
          },
        },
        fill: {
          opacity: 1,
        },
        legend: {
          position: "top",
          horizontalAlign: "left",
          offsetX: 40,
        },
      },
    }
  },
  computed: {
    seriesData() {
      return {
        bio: this.completedDiagnostics.map((d) => getPercentage(d.valueBioHt, d.valueTotalHt)),
        sustainable: this.completedDiagnostics.map((d) => getPercentage(d.valueSustainableHt, d.valueTotalHt)),
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
          color: "#0c7f46",
        },
        {
          name: SUSTAINABLE,
          data: this.seriesData.sustainable,
          color: "#ff8d7e",
        },
        {
          name: OTHER,
          data: this.seriesData.other,
          color: "#999",
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
  },
}

function getPercentage(partialValue, totalValue) {
  if (strictIsNaN(partialValue) || strictIsNaN(totalValue) || totalValue === 0) {
    return null
  } else {
    return Math.round((100 * partialValue) / totalValue)
  }
}

function strictIsNaN(x) {
  return Number(x) !== x
}

function percentageFormatter(val) {
  return val + " %"
}
</script>
